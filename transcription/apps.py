# transcription/apps.py
from django.apps import AppConfig

class TranscriptionConfig(AppConfig):
    name = 'transcription'

    def ready(self):
        try:
            import transcription.signals 
            print("Signals imported successfully")
        except ImportError as e:
            print(f"Error importing signals: {e}")
