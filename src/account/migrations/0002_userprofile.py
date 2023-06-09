# Generated by Django 4.2 on 2023-04-22 08:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                    "gender",
                    models.CharField(choices=[("Male", "Male"), ("Female", "Female")], max_length=6),
                ),
                ("address", models.CharField(blank=True, max_length=255)),
                ("order_history", models.TextField(blank=True)),
                ("payment_method", models.CharField(blank=True, max_length=50)),
                ("social_media_profiles", models.URLField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
