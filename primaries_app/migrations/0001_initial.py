# Generated by Django 4.1.1 on 2023-01-24 12:31

import ckeditor_uploader.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalConfigs",
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
                (
                    "stage",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "ՈՐԱԿԱՎՈՐՄԱՆ ՓՈՒԼ"),
                            ("2", "ՀԻՄՆԱԿԱՆ ՓՈՒԼ․ ՔՆՆԱՐԿՈՒՄՆԵՐ ԵՎ ԸՆՏՐՈՂՆԵՐԻ ԳՐԱՆՑՈՒՄ"),
                            ("3", "ՀԻՄՆԱԿԱՆ ՓՈՒԼ․ ՔՎԵԱՐԿՈՒԹՅՈՒՆ"),
                            (
                                "4",
                                "ԵԶՐԱՓՈԿԻՉ ՓՈՒԼ․ ՔՆՆԱՐԿՈՒՄՆԵՐ ԵՎ ԸՆՏՐՈՂՆԵՐԻ ԳՐԱՆՑՈՒՄ",
                            ),
                            ("5", "ԵԶՐԱՓԱԿԻՉ  ՓՈՒԼ․ ՔՎԵԱՐԿՈՒԹՅՈՒՆ"),
                            (None, "Ոչ ակտիվ փուլ"),
                        ],
                        default=None,
                        max_length=1,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Կարգավորումներ",
                "verbose_name_plural": "Կարգավորումներ",
            },
        ),
        migrations.CreateModel(
            name="MarkModel",
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
                ("content", models.CharField(max_length=2000, verbose_name="Տեքստ")),
                (
                    "mark",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(-2),
                            django.core.validators.MaxValueValidator(5),
                        ],
                        verbose_name="Գնահատական",
                    ),
                ),
            ],
            options={
                "verbose_name": "Վստահություն հայտնելու Ընտրանք",
                "verbose_name_plural": "Վստահություն հայտնելու Ընտրանքներ",
            },
        ),
        migrations.CreateModel(
            name="News",
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
                ("title", models.CharField(max_length=1000, verbose_name="Վերնագիր")),
                (
                    "text",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="Տեքստ"
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/news/",
                        verbose_name="Նկար",
                    ),
                ),
                (
                    "media_url",
                    models.URLField(blank=True, null=True, verbose_name="Մեդյա հղում"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Ստեղծվել է"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Փոփոխվել է"),
                ),
            ],
            options={
                "verbose_name": "Նորություններ",
                "verbose_name_plural": "Նորություններ",
            },
        ),
        migrations.CreateModel(
            name="VotingModel",
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
                ("position", models.IntegerField(verbose_name="Համարը")),
                (
                    "points",
                    models.FloatField(default=None, verbose_name="Միաորների Քանակը"),
                ),
                (
                    "stage",
                    models.IntegerField(default=None, verbose_name="Ընտրության փուլը"),
                ),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.candidateprofile",
                        verbose_name="Թեկնածու",
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.voterprofile",
                        verbose_name="Ընտրող",
                    ),
                ),
            ],
            options={
                "verbose_name": "Քվեարկության արդյունքներ",
                "verbose_name_plural": "Քվեարկության արդյունքներ",
            },
        ),
        migrations.CreateModel(
            name="PayViaImage",
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
                (
                    "picture",
                    models.ImageField(
                        upload_to="payment_images/", verbose_name="Վճառման նկար"
                    ),
                ),
                (
                    "voter_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.voterprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "ՎՃարման Նկարներ",
                "verbose_name_plural": "ՎՃարման Նկարներ",
            },
        ),
        migrations.CreateModel(
            name="EvaluateModel",
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
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate",
                        to="accounts.candidateprofile",
                        verbose_name="Թեկնածու",
                    ),
                ),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="primaries_app.markmodel",
                        verbose_name="Ինչպես է գնահատել՞",
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="voter",
                        to="accounts.voterprofile",
                        verbose_name="Ընտրող",
                    ),
                ),
            ],
            options={
                "verbose_name": "Վստահություն Քվեարկում",
                "verbose_name_plural": "Վստահություն Քվեարկում",
                "unique_together": {("voter", "candidate")},
            },
        ),
    ]
