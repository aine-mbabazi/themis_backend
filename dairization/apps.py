# diarization/apps.py

from django.apps import AppConfig

class DiarizationConfig(AppConfig):
    name = 'diarization'

    def ready(self):
        try:
            import diarization.signals
        except ImportError as e:
            print(f"Error importing signals: {e}")
