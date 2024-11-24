# Generated by Django 4.2.5 on 2024-03-29 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_patients_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')])),
                ('age', models.IntegerField(default=1)),
                ('cp', models.IntegerField(choices=[(0, 'Typical angina'), (1, 'Atypical angina'), (2, 'Non-anginal pain'), (3, 'Asymptomatic')])),
                ('trestbps', models.FloatField(default=0.0)),
                ('chol', models.FloatField(default=0.0)),
                ('fbs', models.BooleanField(default=False)),
                ('thalach', models.FloatField(default=0.0)),
                ('exang', models.BooleanField(default=False)),
                ('oldpeak', models.FloatField(default=0.0)),
                ('slope', models.IntegerField(choices=[(0, 'Upsloping'), (1, 'Flat'), (2, 'Downsloping')])),
                ('ca', models.IntegerField()),
                ('thal', models.IntegerField(choices=[(1, 'Normal'), (2, 'Fixed defect'), (3, 'Reversible defect')])),
                ('target', models.BooleanField(default=False)),
                ('is_healed', models.BooleanField(default=False)),
                ('date_recorded', models.DateField(null=True)),
                ('medicine_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.medicines')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patients')),
            ],
        ),
    ]
