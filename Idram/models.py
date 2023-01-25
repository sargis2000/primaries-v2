import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import VoterProfile


# Create your models here.


class Pay(models.Model):
    EDP_BILL_NO = models.UUIDField(
        primary_key=True, default=uuid.uuid4, verbose_name="ՎՃարման ID"
    )
    profile = models.ForeignKey(
        VoterProfile, on_delete=models.CASCADE, verbose_name="Ընտրողի Էջ"
    )
    EDP_AMOUNT = models.CharField(default="1.00", verbose_name="Գումար", max_length=16)
    EDP_REC_ACCOUNT = models.CharField(
        default=str(settings.EDP_REC_ACCOUNT), verbose_name="Ստացողի ID", max_length=16
    )
    confirmed = models.BooleanField(default=False, verbose_name="Հաստատված է")

    class Meta:
        verbose_name = "ՎՃարումներ"
        verbose_name_plural = "ՎՃարումներ"

    def __str__(self):
        return str(self.EDP_BILL_NO)


@receiver(post_save, sender=Pay)
def post_save_profile(sender, instance, created, **kwargs) -> None:
    profile = instance.profile
    # Checking if the candidate is approved by the admin.
    match instance.EDP_AMOUNT:
        case "2.00":
            profile.votes_count = 1
        case "3.00":
            profile.votes_count = 2
        case "4.00":
            profile.votes_count = 3
        case "5.00":
            profile.votes_count = 4
        case "6.00":
            profile.votes_count = 5
    profile.save()
