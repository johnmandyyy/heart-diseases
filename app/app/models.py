"""
Definition of models.
"""

from django.db import models

# Create your models here.


class Reports(models.Model):

    accuracy = models.FloatField(default = 0.00, null = False)
    precision = models.FloatField(default = 0.00, null = False)
    recall = models.FloatField(default = 0.00, null = False)
    f1_score = models.FloatField(default = 0.00, null = False)

class Patients(models.Model):
    name = models.TextField(null = False)
    middle_name = models.TextField(default = None, null = True)
    last_name = models.TextField(default = None, null = True)
    birth_date = models.DateField(default = None, null  = True)

class Medicines(models.Model):
    medicine_name = models.TextField(null = False)
    instruction = models.TextField(null = False)
