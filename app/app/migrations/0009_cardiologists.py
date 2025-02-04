# Generated by Django 4.2.5 on 2024-11-24 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_patientrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cardiologists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suffixes', models.CharField(max_length=255, null=True)),
                ('license_no', models.CharField(max_length=255)),
                ('e_signature', models.FileField(null=True, upload_to='signatures')),
                ('physician_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
