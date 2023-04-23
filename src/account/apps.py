from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        from account.models import get_user_model
        from account.services.signals import create_user_profile_signal

        post_save.connect(create_user_profile_signal, sender=get_user_model())
