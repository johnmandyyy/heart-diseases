# Generated by Django 4.2.5 on 2024-03-23 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_trainingdataset_medicine_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestingDataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicted_values', models.BooleanField(null=True)),
                ('training_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trainingdataset')),
            ],
        ),
    ]
