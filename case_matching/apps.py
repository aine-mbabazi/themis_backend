from django.apps import AppConfig


class CaseMatchingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'case_matching'

    def ready(self):
        try:
            # Full import path to avoid any potential import errors
            import case_matching.signals  
            print("Case matching signals imported successfully")
        except ImportError as e:
            print(f"Error importing signals: {e}")