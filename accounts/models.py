import datetime
import uuid

from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings
from .utils import send_mailgun_mail
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


gender = (
    ("male", "Արական"),
    ("female", "Իգական"),
)

region = (
    ("Աջափնյակ", "Աջափնյակ"),
    ("Ավան", "Ավան"),
    ("Արաբկիր", "Արաբկիր"),
    ("Դավթաշեն", "Դավթաշեն"),
    ("Էրեբունի", "Էրեբունի"),
    ("Կենտրոն", "Կենտրոն"),
    ("Մալաթիա-Սեբաստիա", "Մալաթիա-Սեբաստիա"),
    ("Նոր Նորք", "Նոր Նորք"),
    ("Նուբարաշեն", "Նուբարաշեն"),
    ("Շենգավիթ", "Շենգավիթ"),
    ("Քանաքեռ-Զեյթուն", "Քանաքեռ-Զեյթուն"),
)


class User(AbstractBaseUser, PermissionsMixin):
    """The User class inherits from AbstractBaseUser and PermissionsMixin"""

    email = models.EmailField(max_length=30, verbose_name="էլ․ հաստցէ", unique=True)
    is_staff = models.BooleanField(default=False, verbose_name="Անձնակազմ")
    is_active = models.BooleanField(default=True, verbose_name="Ակտիվ")
    is_voter = models.BooleanField(default=False, verbose_name="Ընտրող")
    is_candidate = models.BooleanField(default=False, verbose_name="Թեկածու")
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name="Գրանցման Ժամանակը"
    )
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        """
        It returns a string representation of the object.
        """
        return self.get_username()

    class Meta:
        verbose_name = "Օգտատերեր"
        verbose_name_plural = "Օգտատերեր"


class CandidateProfile(models.Model):
    """The CandidateProfile class is a model that inherits from the models.Model class"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=100, verbose_name="Անուն")
    last_name = models.CharField(max_length=100, verbose_name="Ազգանուն")
    birthdate = models.DateField(verbose_name="Ծննդյան օր")
    picture = models.ImageField(upload_to="profile_pictures", verbose_name="Նկար")
    gender = models.CharField(max_length=6, choices=gender, verbose_name="Սեռ")
    phone_number = PhoneNumberField(verbose_name="Հեռախոսահամար")
    region = models.CharField(max_length=16, choices=region, verbose_name="Տարածաշրջան")
    address = models.CharField(max_length=100, verbose_name="Հասցե")
    facebook_url = models.URLField(
        max_length=300, verbose_name="Facebook Հղում", help_text="Facebook account url"
    )
    youtube_url = models.URLField(
        max_length=300,
        verbose_name="YouTube Հղում",
        help_text="Youtube account url",
        null=True,
        blank=True,
    )
    additional_url = models.URLField(
        max_length=300,
        verbose_name="Լրացուցիչ հղում",
        help_text="Additional url",
        null=True,
        blank=True,
    )
    party = models.CharField(
        max_length=200,
        help_text="Կուսակցություն",
        default="Անկուսակցական",
        verbose_name="Կուսակցություն",
    )
    education = RichTextUploadingField(verbose_name="Կրթություն")

    work_experience = RichTextUploadingField(
        verbose_name="Աշխատանքային գործունեություն",
    )
    political_experience = RichTextUploadingField(
        verbose_name="Քաղաքական գործունեություն",
    )
    marital_status = RichTextUploadingField(
        verbose_name="Ընտանեկան կարգավիճակ",
    )
    political_opinion = RichTextUploadingField(
        verbose_name="Ազգային-քաղաքական դիրքորոշումներ",
    )
    yerevan_rebuild = RichTextUploadingField(
        verbose_name="Բարեփոխումներ մայրաքաղաքում",
    )

    is_email_verified = models.BooleanField(
        default=False, verbose_name="Էլ․ Հասցեն հատատված է"
    )

    is_approved = models.BooleanField("Հաստատվել է Ադմինի կողմից։", default=False)
    is_cleaned = False

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_picture(self):
        return mark_safe(f'<img src={self.picture.url} width="90" height="70"')

    get_picture.short_description = "picture"

    class Meta:
        verbose_name = "Թեկնածուների էջեր"
        verbose_name_plural = "Թեկնածուների էջեր"


class VoterProfile(models.Model):
    """This class is a model for the VoterProfile table in the database"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Օգտատեր")
    first_name = models.CharField(max_length=200, verbose_name="Անուն")
    last_name = models.CharField(max_length=200, verbose_name="Ազգանուն")
    phone_number = PhoneNumberField(verbose_name="Հեռախոսահամար")
    birthdate = models.DateField(
        default=datetime.date(1950, 1, 1), verbose_name="Ծննդյան օր"
    )
    address = models.CharField(max_length=100, verbose_name="Հասցե")
    soc_url = models.URLField(max_length=300, verbose_name="Սոցիալական կայքի հղում")
    is_email_verified = models.BooleanField(
        default=False, verbose_name="Էլ․ Հասցեն հատատված է"
    )
    is_paid = models.BooleanField(default=False, verbose_name="ՎՃարել է ")
    votes_count = models.IntegerField(default=None, null=True, blank=True)
    already_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Ընտրողների էջեր"
        verbose_name_plural = "Ընտրողների էջեր"


class CandidatePost(models.Model):
    """The CandidatePost class is a model that inherits from the models.Model class"""

    profile = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        help_text="choice which profile to post",
        verbose_name="Թոկնածու",
    )
    title = models.CharField(max_length=100, verbose_name="Վերնագիր")
    text = RichTextUploadingField("Տեքստ", null=True, blank=True)
    media_path = models.URLField(
        max_length=300, verbose_name="Տեսահոլովակի հղում", null=True, blank=True
    )
    photo = models.ImageField(
        upload_to="media/candidate_post_images/",
        verbose_name="Նկար",
        max_length=200,
        null=True,
        blank=True,
    )
    important = models.BooleanField(
        default=False, verbose_name="Կարևոր", null=True, blank=True
    )

    class Meta:
        verbose_name = "Թեկնածուների Փոստեր"
        verbose_name_plural = "Թեկնածուների Փոստեր"

    def __str__(self):
        """
        It returns a string representation of the object.
        """
        return "Հրապարակում: {0}:  Հեղինակ:{1}".format(
            self.title, self.profile.first_name + " " + self.profile.last_name
        )


@receiver(post_save, sender=VoterProfile)
def post_save_user(sender, instance, created, **kwargs):
    """
    If the user is being created, set the password to the raw password, and then save the user

    :param sender: The model class
    :param instance: The User instance that is about to be saved
    :param created: True if a new record is being created
    """

    user = instance.user
    if instance.is_email_verified is True and instance.is_paid is True:
        user.is_voter = True
    else:
        user.is_voter = False
    user.save()


@receiver(post_save, sender=CandidateProfile)
def post_save_profile(sender, instance, created, **kwargs) -> None:
    """
    If the user is being created, set the password to the raw password, and then save the user

    :param sender: The model class
    :param instance: The User instance that is about to be saved
    :param created: True if a new record is being created
    """
    user = instance.user
    # Checking if the candidate is approved by the admin.
    if instance.is_approved:
        user.is_candidate = True
    else:
        user.is_candidate = False
    user.save()


@receiver(post_delete, sender=CandidateProfile)
def set_false_candidate(sender, instance, using, **kwargs):
    """
    When a user is saved, if they are a candidate, set their is_candidate field to False

    :param sender: The model class
    :param instance: The object being saved
    :param using: The database that is being used
    """
    user = instance.user
    user.is_candidate = False
    user.save()


@receiver(post_delete, sender=VoterProfile)
def set_false_voter(sender, instance, using, **kwargs):
    """
    When a user is deleted, set their is_voter attribute to False

    :param sender: The model class
    :param instance: The instance being saved
    :param using: The database that is being used
    """
    user = instance.user
    user.is_voter = False
    user.save()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )

    send_mailgun_mail(
        form=settings.EMAIL_FROM,
        to=[reset_password_token.user.email],
        message=email_plaintext_message,
        subject="Password Reset for {title}".format(title="primaries.am"),
    )
