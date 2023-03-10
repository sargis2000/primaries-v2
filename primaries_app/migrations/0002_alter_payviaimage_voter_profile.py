# Generated by Django 4.1.1 on 2023-01-24 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_email"),
        ("primaries_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payviaimage",
            name="voter_profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.voterprofile",
                verbose_name="ընտրողի էջ",
            ),
        ),
    ]
