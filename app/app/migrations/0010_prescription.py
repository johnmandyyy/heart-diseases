# Generated by Django 4.2.5 on 2024-11-24 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_cardiologists'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_recorded', models.DateField(null=True)),
                ('notes', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('patiend_record_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patientrecord')),
                ('physician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cardiologists')),
            ],
        ),
    ]