
from django.db import models
from transcription.models import Transcription

class AudioChunk(models.Model):
    transcription = models.ForeignKey(Transcription, on_delete=models.CASCADE)
    chunk_file = models.FileField(upload_to='audio_chunks/')
    chunk_index = models.IntegerField()
    transcription_text = models.TextField(blank=True, null=True)
    diarization_data = models.TextField(blank=True, null=True) 
    status = models.CharField(max_length=20, default='pending')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk {self.chunk_index} for {self.transcription}"
