# Generated by Django 4.1.1 on 2023-01-24 12:31

import ckeditor_uploader.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        default=None,
                        max_length=30,
                        null=True,
                        unique=True,
                        verbose_name="էլ․ հաստցէ",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Անձնակազմ"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Ակտիվ")),
                ("is_voter", models.BooleanField(default=False, verbose_name="Ընտրող")),
                (
                    "is_candidate",
                    models.BooleanField(default=False, verbose_name="Թեկածու"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Գրանցման Ժամանակը",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Օգտատերեր",
                "verbose_name_plural": "Օգտատերեր",
            },
        ),
        migrations.CreateModel(
            name="VoterProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=200, verbose_name="Անուն")),
                (
                    "last_name",
                    models.CharField(max_length=200, verbose_name="Ազգանուն"),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Հեռախոսահամար"
                    ),
                ),
                (
                    "birthdate",
                    models.DateField(
                        default=datetime.date(1950, 1, 1), verbose_name="Ծննդյան օր"
                    ),
                ),
                ("address", models.CharField(max_length=100, verbose_name="Հասցե")),
                (
                    "soc_url",
                    models.URLField(
                        max_length=300, verbose_name="Սոցիալական կայքի հղում"
                    ),
                ),
                (
                    "is_email_verified",
                    models.BooleanField(
                        default=False, verbose_name="Էլ․ Հասցեն հատատված է"
                    ),
                ),
                (
                    "is_paid",
                    models.BooleanField(default=False, verbose_name="ՎՃարել է "),
                ),
                (
                    "votes_count",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("already_voted", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Օգտատեր",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ընտրողների էջեր",
                "verbose_name_plural": "Ընտրողների էջեր",
            },
        ),
        migrations.CreateModel(
            name="CandidateProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100, verbose_name="Անուն")),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="Ազգանուն"),
                ),
                ("birthdate", models.DateField(verbose_name="Ծննդյան օր")),
                (
                    "picture",
                    models.ImageField(
                        upload_to="profile_pictures", verbose_name="Նկար"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Արական"), ("female", "Իգական")],
                        max_length=6,
                        verbose_name="Սեռ",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Հեռախոսահամար"
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=16,
                        verbose_name="Տարածաշրջան",
                    ),
                ),
                ("address", models.CharField(max_length=100, verbose_name="Հասցե")),
                (
                    "facebook_url",
                    models.URLField(
                        help_text="Facebook account url",
                        max_length=300,
                        verbose_name="Facebook Հղում",
                    ),
                ),
                (
                    "youtube_url",
                    models.URLField(
                        blank=True,
                        help_text="Youtube account url",
                        max_length=300,
                        null=True,
                        verbose_name="YouTube Հղում",
                    ),
                ),
                (
                    "additional_url",
                    models.URLField(
                        blank=True,
                        help_text="Additional url",
                        max_length=300,
                        null=True,
                        verbose_name="Լրացուցիչ հղում",
                    ),
                ),
                (
                    "party",
                    models.CharField(
                        default="Անկուսակցական",
                        help_text="Կուսակցություն",
                        max_length=200,
                        verbose_name="Կուսակցություն",
                    ),
                ),
                (
                    "education",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Կրթություն"
                    ),
                ),
                (
                    "work_experience",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Աշխատանքային գործունեություն"
                    ),
                ),
                (
                    "political_experience",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Քաղաքական գործունեություն"
                    ),
                ),
                (
                    "marital_status",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Ընտանեկան կարգավիճակ"
                    ),
                ),
                (
                    "political_opinion",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Ազգային-քաղաքական դիրքորոշումներ"
                    ),
                ),
                (
                    "yerevan_rebuild",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="Բարեփոխումներ մայրաքաղաքում"
                    ),
                ),
                (
                    "is_email_verified",
                    models.BooleanField(
                        default=False, verbose_name="Էլ․ Հասցեն հատատված է"
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(
                        default=False, verbose_name="Հաստատվել է Ադմինի կողմից։"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Թեկնածուների էջեր",
                "verbose_name_plural": "Թեկնածուների էջեր",
            },
        ),
        migrations.CreateModel(
            name="CandidatePost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Վերնագիր")),
                (
                    "text",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="Տեքստ"
                    ),
                ),
                (
                    "media_path",
                    models.URLField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="Տեսահոլովակի հղում",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        max_length=200,
                        null=True,
                        upload_to="media/candidate_post_images/",
                        verbose_name="Նկար",
                    ),
                ),
                (
                    "important",
                    models.BooleanField(
                        blank=True, default=False, null=True, verbose_name="Կարևոր"
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        help_text="choice which profile to post",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.candidateprofile",
                        verbose_name="Թոկնածու",
                    ),
                ),
            ],
            options={
                "verbose_name": "Թեկնածուների Փոստեր",
                "verbose_name_plural": "Թեկնածուների Փոստեր",
            },
        ),
    ]