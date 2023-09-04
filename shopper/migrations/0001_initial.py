# Generated by Django 4.2.1 on 2023-09-04 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopperProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ShopperPersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('state_of_origin', models.CharField(max_length=50)),
                ('lga', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('criminal_record', models.BooleanField()),
                ('driving_skill', models.CharField(blank=True, choices=[('None', "I don't know how to drive"), ('Learner', "I'm currently learning how to drive"), ('Intermediate', 'I have intermediate skills'), ('Expert', 'I am an expert driver')], help_text='How would you rate your driving?', max_length=100, null=True)),
                ('means_of_id', models.CharField(blank=True, choices=[('passport', 'Passport'), ('drivers license', 'Drivers Licence'), ('national id', 'National ID'), ('state id', 'State ID')], help_text='Means of ID?', max_length=100, null=True)),
                ('id_document', models.FileField(upload_to='shopper/id_documents/')),
                ('picture', models.FileField(upload_to='shopper/pictures')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shopper', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personalinfo', to='shopper.shopperprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BankInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=50)),
                ('account_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopper.shopperprofile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
