from django.apps import AppConfig


class HlsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hls_app'

    def ready(self):
        import hls_app.signals 