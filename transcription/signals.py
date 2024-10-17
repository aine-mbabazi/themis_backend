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


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from transcription.models import Transcription
# from diarization.models import DiarizedSegment
# from transcription_chunks.models import AudioChunk
# from django.db import transaction


# @receiver(post_save, sender=Transcription)
# def join_diarized_chunks(sender, instance, **kwargs):
#     """Signal to join diarized chunks into one segment after all chunks are diarized."""
#     if instance.status == 'completed':
#         try:
#             with transaction.atomic():
#                 # Fetch all completed and diarized chunks
#                 chunks = AudioChunk.objects.filter(transcription=instance, status='diarized').order_by('chunk_index')

#                 if chunks.exists():
#                     # Join all diarized chunks together
#                     diarized_text = "\n".join(chunk.diarization_data for chunk in chunks)

#                     # Check if a DiarizedSegment already exists for this transcription
#                     diarized_segment, created = DiarizedSegment.objects.get_or_create(
#                         transcription=instance,
#                         defaults={'diarization_data': diarized_text}
#                     )

#                     if not created:
#                         # If the DiarizedSegment already exists, update its diarization_data
#                         diarized_segment.diarization_data = diarized_text
#                         diarized_segment.save(update_fields=['diarization_data'])

#                     print(f"Joined diarization completed for transcription {instance.id}")
#                 else:
#                     print(f"No diarized chunks found for transcription {instance.id}")

#         except Exception as e:
#             print(f"Error during joining diarized chunks for transcription {instance.id}: {e}")