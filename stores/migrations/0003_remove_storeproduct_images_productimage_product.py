# Generated by Django 4.2.2 on 2023-10-31 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_alter_storeproduct_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeproduct',
            name='images',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='stores.storeproduct'),
            preserve_default=False,
        ),
    ]