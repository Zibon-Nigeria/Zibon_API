# Generated by Django 4.2.2 on 2024-01-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_store_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='city',
        ),
        migrations.RemoveField(
            model_name='store',
            name='state',
        ),
        migrations.AddField(
            model_name='store',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
