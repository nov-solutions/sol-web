from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "user"
    verbose_name = "users and authentication module"

    def ready(self):
        try:
            pass
        except ImportError:
            raise ImportError(
                "UserConfig.ready() failed to import mail."
                "The sol mail module is required for the user module to function."
            )
