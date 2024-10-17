from cases import serializers
from cases.models import Case
from cases import serializers
from cases.models import Case
from rest_framework import serializers
from transcription.models import Transcription
from diarization.models import DiarizedSegment
from transcription_chunks.models import AudioChunk
      

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'is_transcribed']

class AudioChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioChunk
        fields = ['id', 'transcription', 'chunk_file', 'chunk_index', 'transcription_text', 'diarization_data', 'status', 'created_at']
        read_only_fields = ['id', 'transcription_text', 'diarization_data', 'status', 'created_at']


class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id', 'audio_file', 'transcription_text', 'case_name', 'case_number', 'status', 'date_created', 'date_updated']

    def create(self, validated_data):
        return Transcription.objects.create(**validated_data)


class DiarizedSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiarizedSegment
        fields = ['transcription', 'diarization_data', 'date_updated']

        

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'title', 'is_transcribed']
