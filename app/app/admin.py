from django.contrib import admin
from .models import *


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Cardiologists)
class CardiologistsAdmin(admin.ModelAdmin):
    pass


@admin.register(TestingDataSet)
class TestingDataSetAdmin(admin.ModelAdmin):
    pass


@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    pass


@admin.register(Patients)
class PatientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Medicines)
class MedicinesAdmin(admin.ModelAdmin):
    pass


@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainingDataSet)
class TrainingDataSetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sex",
        "age",
        "cp",
        "trestbps",
        "chol",
        "fbs",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
        "target",
        "medicine_id",
        "is_healed",
    )
