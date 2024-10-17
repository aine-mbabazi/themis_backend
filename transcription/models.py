from django.db import models

class Transcription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('chunking', 'Chunking'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    audio_file = models.FileField(upload_to='audio_files/')
    transcription_text = models.TextField(blank=True, null=True)
    case_name = models.CharField(max_length=255, blank=True, null=True)
    case_number = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending') 
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_chunked = models.BooleanField(default=False)

    def __str__(self):
        return self.case_name or f"Transcription {self.id}"
