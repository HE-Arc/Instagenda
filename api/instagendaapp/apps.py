from django.apps import AppConfig


class InstagendaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instagendaapp'

    def ready(self):
        import instagendaapp.signals