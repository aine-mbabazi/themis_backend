# transcription/apps.py
from django.apps import AppConfig

class TranscriptionConfig(AppConfig):
    name = 'transcription'

    def ready(self):
        try:
            # Use the full import path to avoid any potential import errors
            import transcription.signals  # Ensure that signals are imported and registered
            print("Signals imported successfully")
        except ImportError as e:
            print(f"Error importing signals: {e}")
