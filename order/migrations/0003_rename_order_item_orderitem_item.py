# Generated by Django 4.2.2 on 2024-02-19 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_is_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_item',
            new_name='item',
        ),
    ]
