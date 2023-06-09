# Generated by Django 4.2.1 on 2023-06-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_alter_store_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeinventory',
            name='price',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=5),
        ),
    ]
