from django.db import models

# Create your models here.


from django.db import models
from transcription.models import Transcription

class DiarizedSegment(models.Model):
    transcription = models.OneToOneField(Transcription, on_delete=models.CASCADE)
    diarization_data = models.TextField(blank=True, null=True)  # This will be filled automatically
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diarized Segment for {self.transcription.case_name or 'Audio'}"
