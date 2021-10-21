from django.apps import AppConfig


class UcclmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ucclms'

    def ready(self):
        import ucclms.signals
