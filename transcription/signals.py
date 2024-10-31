from django.db.models.signals import post_save
from django.dispatch import receiver
from pydub import AudioSegment
from transcription.models import Transcription
from transcription_chunks.models import AudioChunk

@receiver(post_save, sender=Transcription)
def auto_chunk_audio(sender, instance, created, **kwargs):
    """Chunks the audio file when a new Transcription is created."""
    print(f"Signal received for Transcription: {instance.id}")  # Debugging line
    
    if created and instance.audio_file and not instance.is_chunked:
        try:
            # Load the audio file
            audio = AudioSegment.from_file(instance.audio_file.path)
            chunk_length_ms = 2 * 60 * 1000  # Chunk size of 5 minutes
            chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

            # Create an AudioChunk object for each chunk
            for index, chunk in enumerate(chunks):
                chunk_file_path = f"audio_chunks/{instance.id}_chunk_{index}.wav"
                chunk.export(chunk_file_path, format="wav")

                AudioChunk.objects.create(
                    transcription=instance,
                    chunk_file=chunk_file_path,
                    chunk_index=index
                )

                print(f"Created chunk {index} for transcription {instance.id}")  # Debugging line

            # Update transcription status
            instance.is_chunked = True
            instance.status = 'in_progress'
            instance.save(update_fields=['is_chunked', 'status'])

        except Exception as e:
            instance.status = 'failed'
            instance.save(update_fields=['status'])
            print(f"Error chunking audio file for transcription {instance.id}: {e}")


