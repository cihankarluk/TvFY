from django.apps import AppConfig


class SeriesConfig(AppConfig):
    name = 'TvFY.series'

    def ready(self):
        from TvFY.series import signals
