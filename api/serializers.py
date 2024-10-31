
from rest_framework import serializers
from transcription.models import Transcription
from diarization.models import DiarizedSegment
from transcription_chunks.models import AudioChunk
from case_matching.models import Case_matching

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

class CaseMatchingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Case_matching
        fields = ['transcription', 'date_created', 'case']

    def create(self, validated_data):
        transcription = validated_data.get('transcription')
        if not isinstance(transcription, (str, bytes)):
            raise serializers.ValidationError("Transcription must be a string or bytes-like object.")
        return super().create(validated_data)
