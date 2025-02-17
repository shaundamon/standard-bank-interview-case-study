from django.apps import AppConfig


class MLConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'

    def ready(self):
        """Initialize ML models when Django starts."""
        from .models.clip import initialize_clip_model
        initialize_clip_model()
