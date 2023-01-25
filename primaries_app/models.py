from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from accounts.models import CandidateProfile, User, VoterProfile
from accounts.utils import send_mailgun_mail


class MarkModel(models.Model):
    """A model for creating texts and marks for evaluating candidates"""

    content = models.CharField(max_length=2000, verbose_name="Տեքստ")
    mark = models.SmallIntegerField(
        validators=[MinValueValidator(-2), MaxValueValidator(5)],
        verbose_name="Գնահատական",
    )

    class Meta:
        verbose_name = "Վստահություն հայտնելու Ընտրանք"
        verbose_name_plural = "Վստահություն հայտնելու Ընտրանքներ"

    def __str__(self):
        return self.content[:30]


class EvaluateModel(models.Model):
    """Evaluating Candidates"""

    voter = models.ForeignKey(
        VoterProfile,
        on_delete=models.CASCADE,
        related_name="voter",
        verbose_name="Ընտրող",
    )
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="candidate",
        verbose_name="Թեկնածու",
    )
    poll = models.ForeignKey(
        MarkModel, on_delete=models.CASCADE, verbose_name="Ինչպես է գնահատել՞"
    )

    def clean(self):
        """
            Check if requested user candidate
        :return: if requested user not  candidate  raise error
        """
        if self.candidate.user not in User.objects.filter(is_candidate=True):
            raise ValidationError("Can vote only for candidates")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(EvaluateModel, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            "voter",
            "candidate",
        )
        verbose_name = "Վստահություն Քվեարկում"
        verbose_name_plural = "Վստահություն Քվեարկում"


class News(models.Model):
    title = models.CharField(max_length=1000, verbose_name="Վերնագիր")
    text = RichTextUploadingField(blank=True, null=True, verbose_name="Տեքստ")
    picture = models.ImageField(
        upload_to="media/news/", blank=True, null=True, verbose_name="Նկար"
    )
    media_url = models.URLField(blank=True, null=True, verbose_name="Մեդյա հղում")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ստեղծվել է")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Փոփոխվել է")

    def get_picture(self):
        return mark_safe(f'<img src={self.picture.url} width="90" height="70"')

    get_picture.short_description = "picture"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Նորություններ"
        verbose_name_plural = "Նորություններ"


class GlobalConfigs(models.Model):
    stage = models.CharField(
        choices=(
            ("1", "ՈՐԱԿԱՎՈՐՄԱՆ ՓՈՒԼ"),
            ("2", "ՀԻՄՆԱԿԱՆ ՓՈՒԼ․ ՔՆՆԱՐԿՈՒՄՆԵՐ ԵՎ ԸՆՏՐՈՂՆԵՐԻ ԳՐԱՆՑՈՒՄ"),
            ("3", "ՀԻՄՆԱԿԱՆ ՓՈՒԼ․ ՔՎԵԱՐԿՈՒԹՅՈՒՆ"),
            ("4", "ԵԶՐԱՓՈԿԻՉ ՓՈՒԼ․ ՔՆՆԱՐԿՈՒՄՆԵՐ ԵՎ ԸՆՏՐՈՂՆԵՐԻ ԳՐԱՆՑՈՒՄ"),
            ("5", "ԵԶՐԱՓԱԿԻՉ  ՓՈՒԼ․ ՔՎԵԱՐԿՈՒԹՅՈՒՆ"),
            (None, "Ոչ ակտիվ փուլ"),
        ),
        blank=True,
        null=True,
        default=None,
        max_length=1,
    )

    def __str__(self):
        return "Կարգավորումներ"

    class Meta:
        verbose_name = "Կարգավորումներ"
        verbose_name_plural = "Կարգավորումներ"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(GlobalConfigs, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


@receiver(post_save, sender=GlobalConfigs)
def post_save_confs(sender, instance, **kwargs) -> None:
    set_unpaid = ["1", "2", "4", None]

    if (
        instance.stage in set_unpaid
        and GlobalConfigs.objects.get(id=1).stage != instance.stage
    ):
        VoterProfile.objects.all().update(
            is_paid=False, votes_count=None, already_voted=False
        )
        User.objects.all().update(is_voter=False)


class VotingModel(models.Model):
    voter = models.ForeignKey(
        VoterProfile, on_delete=models.CASCADE, verbose_name="Ընտրող"
    )
    candidate = models.ForeignKey(
        CandidateProfile, on_delete=models.CASCADE, verbose_name="Թեկնածու"
    )
    position = models.IntegerField(verbose_name="Համարը")
    points = models.FloatField(default=None, verbose_name="Միաորների Քանակը")
    stage = models.IntegerField(default=None, verbose_name="Ընտրության փուլը")

    class Meta:
        verbose_name = "Քվեարկության արդյունքներ"
        verbose_name_plural = "Քվեարկության արդյունքներ"


class PayViaImage(models.Model):
    voter_profile = models.ForeignKey(
        VoterProfile, on_delete=models.CASCADE, verbose_name="ընտրողի էջ"
    )
    picture = models.ImageField(
        upload_to="payment_images/", verbose_name="Վճառման նկար"
    )

    def __str__(self):
        return (
            self.voter_profile.first_name + " " + self.voter_profile.last_name + "նկար"
        )

    class Meta:
        verbose_name = "ՎՃարման Նկարներ"
        verbose_name_plural = "ՎՃարման Նկարներ"

    def get_voter_profile_full_name(self):
        return self.voter_profile.first_name + " " + self.voter_profile.last_name

    get_voter_profile_full_name.short_description = "Ընտրողի էջ"

    def get_picture(self):
        return mark_safe(f'<img src={self.picture.url} width="90" height="70"')

    get_picture.short_description = "picture"


@receiver(post_save, sender=PayViaImage)
def post_save_image(sender, instance, created, **kwargs) -> None:
    if created:
        send_mailgun_mail(
            form=instance.voter_profile.user.email,
            to=settings.ADMIN_EMAIL,
            subject="ՎՃարում",
            message=f"{instance.get_voter_profile_full_name} ընտրողը ուղղարկել է"
            f" վճարման կտրոն խնդրում ենք ստուգեք այն և հաստատեք նրա ընտրողի կարգավիճակը։",
        )
