from django.db import models
from transcription.models import Transcription

class Case_matching(models.Model):
    case = models.JSONField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    transcription = models.OneToOneField(Transcription, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"Case Brief_{self.id}")