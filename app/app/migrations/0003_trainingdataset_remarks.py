# Generated by Django 4.2.5 on 2024-03-23 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_trainingdataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingdataset',
            name='remarks',
            field=models.IntegerField(choices=[(0, 'Normal'), (1, 'Abnormal')], default=0),
        ),
    ]
