from django.db import models
from transcription.models import Transcription

# Define the CaseBrief model
class CaseBrief(models.Model):
    transcription = models.ForeignKey(Transcription, on_delete=models.CASCADE, related_name='case_briefs')
    case_title = models.CharField(max_length=255, blank=True, default=".......")
    case_number = models.CharField(max_length=100, blank=True, default=".......")
    judge_name = models.CharField(max_length=255, blank=True, default=".......")
    accused_name = models.CharField(max_length=255, blank=True, default=".......")
    filtered_transcript = models.TextField(blank=True, default=".......")
    court_type = models.CharField(max_length=255, blank=True, default=".......")
    country = models.CharField(max_length=100, blank=True, default=".......")
    court_location = models.CharField(max_length=255, blank=True, default=".......")
    date = models.CharField(max_length=100, blank=True, default=".......")
    prosecutor_name = models.CharField(max_length=255, blank=True, default=".......")
    defense_counsel_name = models.CharField(max_length=255, blank=True, default=".......")
    charges = models.TextField(blank=True, default=".......")
    plea = models.TextField(blank=True, default=".......")
    verdict = models.TextField(blank=True, default=".......")
    sentence = models.TextField(blank=True, default=".......")
    mitigating_factors = models.TextField(blank=True, default=".......")
    aggravating_factors = models.TextField(blank=True, default=".......")
    legal_principles = models.TextField(blank=True, default=".......")
    precedents_cited = models.TextField(blank=True, default=".......")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case Brief for {self.transcription.case_name or 'Unknown Case'}"
