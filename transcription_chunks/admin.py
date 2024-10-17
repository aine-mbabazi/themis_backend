# from django.contrib import admin
# from transcription_chunks.models import AudioChunk

# @admin.register(AudioChunk)
# class AudioChunkAdmin(admin.ModelAdmin):
#     list_display = ('transcription', 'chunk_index', 'status', 'created_at')  # Display these fields in the admin list view
#     list_filter = ('status', 'created_at')  # Add filters to allow filtering by status and creation date
#     search_fields = ('transcription__case_name', 'transcription__case_number')  # Add search by case name or number
#     ordering = ('-created_at',)  # Order by creation date (newest first)



from django.contrib import admin
from transcription_chunks.models import AudioChunk

@admin.register(AudioChunk)
class AudioChunkAdmin(admin.ModelAdmin):
    list_display = ('transcription', 'chunk_index', 'status', 'has_diarization', 'created_at')  # Show diarization status
    list_filter = ('status', 'created_at')  # Filter by status and creation date
    search_fields = ('transcription__case_name', 'transcription__case_number', 'chunk_index')  # Search by transcription and chunk index
    ordering = ('-created_at',)  # Order by latest

    # Ensure transcription_text and diarization_data are displayed in the form
    fields = ('transcription', 'chunk_file', 'chunk_index', 'transcription_text', 'diarization_data', 'status', 'created_at')
    readonly_fields = ('created_at', 'transcription_text', 'diarization_data')  # Make fields read-only in the form

    # Method to display whether diarization is available
    def has_diarization(self, obj):
        return bool(obj.diarization_data)
    has_diarization.boolean = True  # Display as a boolean icon
    has_diarization.short_description = 'Diarized'