from django.apps import AppConfig


class SpectacularSwaggerConfig(AppConfig):
    name = "spectacular"
    verbose_name = "spectacular swagger docs"

    def ready(self):
        try:
            import drf_spectacular  # noqa: F401
        except ImportError:
            raise ImportError(
                "SpectacularSwaggerConfig.ready() failed to import drf_spectacular. "
                "The drf_spectacular module is required for the spectacular module to function."
            )
