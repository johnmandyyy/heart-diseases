"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User


class Cardiologists(models.Model):
    physician_account = models.ForeignKey(User, on_delete=models.CASCADE)
    suffixes = models.CharField(max_length=255, null=True)
    license_no = models.CharField(max_length=255, null=False)
    e_signature = models.FileField(null=True, upload_to="signatures")

    def __str__(self):
        return (
            str(self.physician_account.first_name)
            + " "
            + str(self.physician_account.last_name)
            + " "
            + str(self.suffixes)
        )


class Reports(models.Model):

    accuracy = models.FloatField(default=0.00, null=False)
    precision = models.FloatField(default=0.00, null=False)
    recall = models.FloatField(default=0.00, null=False)
    f1_score = models.FloatField(default=0.00, null=False)

    def save(self, *args, **kwargs):
        self.accuracy = round(self.accuracy, 2)
        self.precision = round(self.precision, 2)
        self.recall = round(self.recall, 2)
        self.f1_score = round(self.f1_score, 2)
        super().save(*args, **kwargs)


class Patients(models.Model):

    SEX_CHOICES = ((0, "Male"), (1, "Female"))

    name = models.TextField(null=False)
    middle_name = models.TextField(default=None, null=True)
    last_name = models.TextField(default=None, null=True)
    birth_date = models.DateField(default=None, null=True)
    sex = models.IntegerField(choices=SEX_CHOICES, default=None, null=True)

    def __str__(self):
        return self.last_name + ", " + self.name + " " + self.middle_name


class Medicines(models.Model):

    medicine_name = models.TextField(null=False)
    instruction = models.TextField(null=False)

    def __str__(self):
        return f"{self.medicine_name}"


class TrainingDataSet(models.Model):
    # Chest Pain types
    CP_CHOICES = (
        (0, "Typical angina"),
        (1, "Atypical angina"),
        (2, "Non-anginal pain"),
        (3, "Asymptomatic"),
    )

    SLOPE_CHOICES = ((0, "Upsloping"), (1, "Flat"), (2, "Downsloping"))

    THAL_CHOICES = ((1, "Normal"), (2, "Fixed defect"), (3, "Reversible defect"))

    CP_CHOICES = (
        (0, "Typical angina"),
        (1, "Atypical angina"),
        (2, "Non-anginal pain"),
        (3, "Asymptomatic"),
    )

    SEX_CHOICES = ((0, "Male"), (1, "Female"))

    sex = models.IntegerField(choices=SEX_CHOICES)
    age = models.IntegerField(default=1)
    cp = models.IntegerField(choices=CP_CHOICES)
    trestbps = models.FloatField(default=0.00)
    chol = models.FloatField(default=0.00)
    fbs = models.BooleanField(default=False)
    thalach = models.FloatField(default=0.00)
    exang = models.BooleanField(default=False)
    oldpeak = models.FloatField(default=0.00)
    slope = models.IntegerField(choices=SLOPE_CHOICES)
    ca = models.IntegerField()
    thal = models.IntegerField(choices=THAL_CHOICES)
    target = models.BooleanField(default=False)
    medicine_id = models.ForeignKey(Medicines, on_delete=models.CASCADE, null=True)
    is_healed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        self.trestbps = round(self.trestbps, 2)
        self.chol = round(self.chol, 2)
        self.thalach = round(self.thalach, 2)
        self.oldpeak = round(self.oldpeak, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Heart Health Data - ID: {self.pk}"


class TestingDataSet(models.Model):
    training_id = models.ForeignKey(TrainingDataSet, on_delete=models.CASCADE)
    predicted_values = models.BooleanField(null=True)


class PatientRecord(models.Model):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)

    sex = models.IntegerField(choices=TrainingDataSet.SEX_CHOICES)
    age = models.IntegerField(default=1)
    cp = models.IntegerField(choices=TrainingDataSet.CP_CHOICES)
    trestbps = models.FloatField(default=0.00)
    chol = models.FloatField(default=0.00)
    fbs = models.BooleanField(default=False)
    thalach = models.FloatField(default=0.00)
    exang = models.BooleanField(default=False)
    oldpeak = models.FloatField(default=0.00)
    slope = models.IntegerField(choices=TrainingDataSet.SLOPE_CHOICES)
    ca = models.IntegerField()
    thal = models.IntegerField(choices=TrainingDataSet.THAL_CHOICES)
    target = models.BooleanField(default=False)
    medicine_id = models.ForeignKey(Medicines, on_delete=models.CASCADE, null=True)
    is_healed = models.BooleanField(default=False)
    date_recorded = models.DateField(null=True)

    def __str__(self):
        return (
            str(self.pk)
            + " # "
            + " "
            + self.patient_id.last_name
            + ", "
            + self.patient_id.name
            + " "
            + self.patient_id.middle_name
        )


class Prescription(models.Model):

    patiend_record_id = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)
    date_recorded = models.DateField(null=True)
    notes = models.TextField(null=True)
    description = models.TextField(null=True)
    physician = models.ForeignKey(Cardiologists, on_delete=models.CASCADE)

    def __str__(self):
        return (
            str(self.pk)
            + "-"
            + str(self.patiend_record_id.pk)
            + "-"
            + str(self.date_recorded)
        )
