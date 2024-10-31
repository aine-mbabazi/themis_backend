from django.db.models.signals import post_save
from django.dispatch import receiver
from transcription.models import Transcription
from diarization.models import DiarizedSegment
from transcription_chunks.models import AudioChunk
from django.db import transaction

@receiver(post_save, sender=Transcription)
@receiver(post_save, sender=Transcription)
def join_diarized_chunks(sender, instance, **kwargs):
    """Signal to join diarized chunks into one segment after all chunks are diarized."""
    if instance.status == 'completed':
        try:
            with transaction.atomic():
                # Fetch all completed and diarized chunks
                chunks = AudioChunk.objects.filter(transcription=instance, status='diarized').order_by('chunk_index')

                if chunks.exists():
                    # Join all diarized chunks together
                    diarized_text = "\n".join(chunk.diarization_data for chunk in chunks)

                    # Check if a DiarizedSegment already exists for this transcription
                    diarized_segment, created = DiarizedSegment.objects.get_or_create(
                        transcription=instance,
                        defaults={'diarization_data': diarized_text}
                    )

                    if not created:
                        # If the DiarizedSegment already exists, update its diarization_data
                        diarized_segment.diarization_data = diarized_text
                        diarized_segment.save(update_fields=['diarization_data'])

                    print(f"Joined diarization completed for transcription {instance.id}")
                else:
                    print(f"No diarized chunks found for transcription {instance.id}")

        except Exception as e:
            print(f"Error during joining diarized chunks for transcription {instance.id}: {e}")