# Generated by Django 4.2.2 on 2024-01-29 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_remove_store_city_remove_store_state_store_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeproduct',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
