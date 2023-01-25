from django.apps import AppConfig


def create_config(sender, **kwargs):
    from .models import GlobalConfigs

    GlobalConfigs.objects.get_or_create(id=1)


class PrimariesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "primaries_app"
    verbose_name = "ՆԱԽԸՆՏՐՈՒԹՅՈՒՆ"

    def ready(self):
        """
        It connects the create_config function to the post_migrate signal, which is sent by the sender (the app)
        """
        from django.db.models.signals import post_migrate

        post_migrate.connect(create_config, sender=self)
