from django.apps import AppConfig


class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campaigns'
    verbose_name = 'Campañas'

    def ready(self):
        import campaigns.signals  # noqa: F401
