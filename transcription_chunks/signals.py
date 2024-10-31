from django.db.models.signals import post_save
from django.dispatch import receiver
from transcription_chunks.models import AudioChunk
from api.utils import transcribe_audio_with_retry, diarize_audio_with_retry, format_diarization
from django.db import transaction




# Function to append chunk transcription to the parent Transcription model
def append_to_transcription(transcription, chunk_text):
    """Appends chunk text to the parent Transcription model."""
    if transcription.transcription_text:
        # Append the new chunk transcription to the existing transcription text
        transcription.transcription_text += "\n" + chunk_text
    else:
        # If no transcription text exists yet, start with the first chunk
        transcription.transcription_text = chunk_text

    transcription.save(update_fields=['transcription_text'])
    print(f"Updated Transcription ID {transcription.id} with new chunk.")

# Function to transcribe individual chunks
def transcribe_chunk(chunk):
    """Transcribe a single chunk with retry mechanism and update parent Transcription model."""
    print(f"Attempting to transcribe chunk {chunk.chunk_index}") 

    if chunk.chunk_file and chunk.status == 'pending':
        try:
            with transaction.atomic():
                print(f"Processing chunk {chunk.chunk_index}") 
                chunk.status = 'processing'
                chunk.save(update_fields=['status'])

                # Transcribe the chunk using retry logic
                transcription_text = transcribe_audio_with_retry(chunk.chunk_file.path)

                if transcription_text:
                    chunk.transcription_text = transcription_text
                    chunk.status = 'completed'
                    print(f"Transcription successful for chunk {chunk.chunk_index}") 

                    # Append the chunk's transcribed text to the parent Transcription model
                    append_to_transcription(chunk.transcription, transcription_text)
                else:
                    chunk.status = 'failed'
                    print(f"Transcription failed for chunk {chunk.chunk_index}") 

                # Save the updated chunk status and transcription text to the database
                chunk.save(update_fields=['transcription_text', 'status'])
                print(f"Chunk {chunk.chunk_index} saved with status: {chunk.status}") 

        except Exception as e:
            chunk.status = 'failed'
            chunk.save(update_fields=['status'])
            print(f"Error processing audio chunk {chunk.chunk_index}: {e}")

    # Checking if all chunks are completed
    incomplete_chunks = AudioChunk.objects.filter(transcription=chunk.transcription, status__in=['pending', 'processing']).exists()
    if not incomplete_chunks:
        chunk.transcription.status = 'completed'
        chunk.transcription.save(update_fields=['status'])
        print(f"Transcription {chunk.transcription.id} marked as completed.")
    else:
        chunk.transcription.status = 'in_progress'
        chunk.transcription.save(update_fields=['status'])
        print(f"Transcription {chunk.transcription.id} is still in progress.")


# Signal to handle audio chunk creation and trigger transcription
@receiver(post_save, sender=AudioChunk)
def auto_transcribe_chunk(sender, instance, created, **kwargs):
    """Signal to transcribe chunk when a new AudioChunk is created."""
    print(f"Signal received for AudioChunk: {instance.chunk_index}") 

    if created:
        chunks = AudioChunk.objects.filter(transcription=instance.transcription, status='pending')

        for chunk in chunks:
            transcribe_chunk(chunk)

        # Checking if all chunks for the transcription have been completed
        incomplete_chunks = AudioChunk.objects.filter(transcription=instance.transcription, status__in=['pending', 'processing']).exists()
        
        if not incomplete_chunks:
            # If no incomplete chunks, mark the transcription as completed
            instance.transcription.status = 'completed'
            instance.transcription.save(update_fields=['status'])
            print(f"Transcription {instance.transcription.id} marked as completed.")





@receiver(post_save, sender=AudioChunk)
def auto_diarize_chunk(sender, instance, created, **kwargs):
    """Signal to diarize a chunk when transcription is completed."""
    if instance.status == 'completed' and instance.chunk_file:
        try:
            print(f"Performing diarization for chunk {instance.chunk_index} of transcription {instance.transcription.id}")
            
            diarization_data = diarize_audio_with_retry(instance.chunk_file.path)
            
            if diarization_data:
                # Now move into transaction block after diarization is successful
                with transaction.atomic():
                    formatted_data = format_diarization(diarization_data)
                    instance.diarization_data = formatted_data
                    instance.status = 'diarized'
                    instance.save(update_fields=['diarization_data', 'status'])
                    print(f"Diarization completed for chunk {instance.chunk_index}")
            else:
                instance.status = 'failed'
                instance.save(update_fields=['status'])
                print(f"Diarization failed for chunk {instance.chunk_index}")

        except Exception as e:
            instance.status = 'failed'
            instance.save(update_fields=['status'])
            print(f"Error during diarization for chunk {instance.chunk_index}: {e}")