from django.apps import AppConfig

class TranscriptionChunksConfig(AppConfig):
    name = 'transcription_chunks'

    def ready(self):
        try:
            # Use the full import path to avoid any potential import errors
            import transcription_chunks.signals  # Ensure that signals are imported and registered
            print("signals imported successfully")
        except ImportError as e:
            print(f"Error importing transcription_chunks signals: {e}")
