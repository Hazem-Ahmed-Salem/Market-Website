from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AI'
    def ready(self):
        # Initialize model loader when Django starts
        from .ml_utils.model_loader import ModelLoader
        ModelLoader.get_instance()  # Loads model but waits to fit encoder