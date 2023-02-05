from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assessment.apps.manager'

    def ready(self):                # NEW
        import assessment.apps.manager.signals     # NEW
