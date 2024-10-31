
from rest_framework import generics, viewsets, status, mixins
from .serializers import TranscriptionSerializer, DiarizedSegmentSerializer, AudioChunkSerializer, CaseMatchingSerializers
from transcription.models import Transcription
from diarization.models import DiarizedSegment
from transcription_chunks.models import AudioChunk
from case_matching.models import Case_matching
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound
from case_matching.signals import scrape_case_laws, extract_case_details
from django.db.models import Count


class TranscriptionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    This viewset provides `list`, `create`, and `retrieve` actions for Transcriptions.
    """
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        """
        Handle audio file upload and trigger transcription.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            transcription = serializer.save()
            return Response({
                'id': transcription.id,
                'message': 'Transcription processed successfully.',
                'status': transcription.status,
                'transcription_text': transcription.transcription_text,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_transcription(self, request, pk=None):
        """
        Return the transcription status and text.
        """
        transcription = self.get_object()
        return Response({
            'id': transcription.id,
            'status': transcription.status,
            'transcription_text': transcription.transcription_text,
        })
        
        
        
    @action(detail=False, methods=['get'])
    def transcription_status_counts(self, request):
        """
        Return the count of transcriptions with statuses 'completed' and 'pending'.
        """
        counts = Transcription.objects.values('status').annotate(total=Count('status'))
        completed_count = next((item['total'] for item in counts if item['status'] == 'completed'), 0)
        pending_count = next((item['total'] for item in counts if item['status'] == 'pending'), 0)
        
        return Response({
            'completed': completed_count,
            'pending': pending_count,
        }, status=status.HTTP_200_OK)
        
        


class TranscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific transcription.
    """
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def get_object(self):
        """
        Custom method to get a transcription by ID or raise a 404 error if not found.
        """
        try:
            transcription = Transcription.objects.get(id=self.kwargs['pk'])
            return transcription
        except Transcription.DoesNotExist:
            raise NotFound({"error": "Transcription not found"})


class DiarizedSegmentListCreateView(generics.ListCreateAPIView):
    """
    Handles the creation and listing of diarized segments.
    """
    queryset = DiarizedSegment.objects.all()
    serializer_class = DiarizedSegmentSerializer


class DiarizationDetailView(generics.RetrieveAPIView):
    """
    Retrieve diarization for a specific transcription.
    """
    queryset = DiarizedSegment.objects.all()
    serializer_class = DiarizedSegmentSerializer

    def get(self, request, pk):
        try:
            diarization = DiarizedSegment.objects.get(transcription__id=pk)
            serializer = DiarizedSegmentSerializer(diarization)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DiarizedSegment.DoesNotExist:
            return Response({"error": "Diarization not found for this transcription"}, status=status.HTTP_404_NOT_FOUND)



class CaseMatchingListView(generics.ListCreateAPIView):
    queryset = Case_matching.objects.all()
    serializer_class = CaseMatchingSerializers

    def post(self, request):
        transcription_id = request.data.get("transcription")
        print(f'ID: {request.data}')

        if not transcription_id:
            return Response({"error": "Transcription ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract transcription text using the ID
            transcription = Transcription.objects.get(id=transcription_id)
            transcription_text = transcription.transcription_text

            extracted_details = extract_case_details(transcription_text)
            search_term = ' '.join(extracted_details)

            case_laws = scrape_case_laws(search_term)

            # Create a new Case_matching instance
            case_matching = Case_matching.objects.create(
                transcription=transcription,
                case={"details": extracted_details, "related_cases": case_laws}
            )
            
            serializer = CaseMatchingSerializers(case_matching)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Transcription.DoesNotExist:
            return Response({"error": "Transcription not found"}, status=status.HTTP_404_NOT_FOUND)



class CaseMatchingDetailView(generics.RetrieveAPIView):
    queryset = Case_matching.objects.all()
    serializer_class = CaseMatchingSerializers
    def get(self, request, id):
        try:
           case_law = Case_matching.objects.get(transcription_id=id)
           serializer = CaseMatchingSerializers(case_law)
           return Response(serializer.data, status=status.HTTP_200_OK)

        except Case_matching.DoesNotExist:
            return Response({"error": "Diarization not found for this transcription"}, status=status.HTTP_404_NOT_FOUND)


class AudioChunkViewSet(viewsets.ModelViewSet):
    """
    A viewset to handle creating, retrieving, and listing audio chunks.
    """
    queryset = AudioChunk.objects.all()
    serializer_class = AudioChunkSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle uploading a new audio chunk.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            audio_chunk = serializer.save()
            return Response({
                'id': audio_chunk.id,
                'transcription_id': audio_chunk.transcription.id,
                'chunk_index': audio_chunk.chunk_index,
                'status': audio_chunk.status,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Return a specific audio chunk.
        """
        chunk = self.get_object()
        return Response({
            'id': chunk.id,
            'transcription_id': chunk.transcription.id,
            'chunk_index': chunk.chunk_index,
            'status': chunk.status,
            'transcription_text': chunk.transcription_text,
            'diarization_data': chunk.diarization_data,
        })

    def list(self, request, *args, **kwargs):
        """
        Return a list of audio chunks.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from django.shortcuts import render, get_object_or_404, redirect
from transcription.models import Transcription


def generate_case_brief_view(request, transcription_id):
    transcription = get_object_or_404(Transcription, id=transcription_id)

    # Generate PDF file for the case brief
    pdf_filename = f"case_brief_{transcription.case_number}.pdf"
    image_path = "/home/student/Downloads/themis_logo.png"  

    # Redirect or render a success message (based on your requirement)
    return redirect('case_brief_success')

