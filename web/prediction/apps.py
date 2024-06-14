from django.apps import AppConfig


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web.prediction'
    
    def ready(self):
        import web.prediction.signals
