# Generated by Django 4.2 on 2023-04-29 16:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("craft", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["user"]},
        ),
    ]