# Generated by Django 4.2 on 2023-04-24 06:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("craft", "0002_alter_category_options_remove_product_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
    ]
