# Generated by Django 4.2.2 on 2023-12-04 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_remove_storeproduct_category_storeproduct_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='latitube',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='longitude',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]