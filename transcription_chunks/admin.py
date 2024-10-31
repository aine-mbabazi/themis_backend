
from django.contrib import admin
from transcription_chunks.models import AudioChunk

@admin.register(AudioChunk)
class AudioChunkAdmin(admin.ModelAdmin):
    list_display = ('transcription', 'chunk_index', 'status', 'has_diarization', 'created_at') 
    list_filter = ('status', 'created_at')  
    search_fields = ('transcription__case_name', 'transcription__case_number', 'chunk_index') 
    ordering = ('-created_at',)  

    # Ensure transcription_text and diarization_data are displayed in the form
    fields = ('transcription', 'chunk_file', 'chunk_index', 'transcription_text', 'diarization_data', 'status', 'created_at')
    readonly_fields = ('created_at', 'transcription_text', 'diarization_data')  

    # Method to display whether diarization is available
    def has_diarization(self, obj):
        return bool(obj.diarization_data)
    has_diarization.boolean = True  
    has_diarization.short_description = 'Diarized'