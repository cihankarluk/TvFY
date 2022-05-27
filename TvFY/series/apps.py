from django.apps import AppConfig


class SeriesConfig(AppConfig):
    name = "TvFY.series"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from TvFY.series import signals
