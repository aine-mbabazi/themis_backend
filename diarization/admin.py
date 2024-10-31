from django.contrib import admin
from diarization.models import DiarizedSegment


@admin.register(DiarizedSegment)
class DiarizedSegmentAdmin(admin.ModelAdmin):
    list_display = ['transcription'] 
    search_fields = ['transcription__case_name', 'transcription__case_number']  
    readonly_fields = ['diarization_data']  

    # Display full diarization data and make it read-only
    fields = ['transcription', 'diarization_data']

    
