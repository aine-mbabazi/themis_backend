from django.contrib import admin
from .models import Transcription

@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ['case_name','case_number','status', 'audio_file', 'date_created']
    readonly_fields = ['transcription_text'] 
