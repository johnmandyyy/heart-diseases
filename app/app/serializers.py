from rest_framework import serializers
from .models import *


class GenerateDataSetSerializer(serializers.Serializer):
    is_generate = serializers.BooleanField()

class TrainHeartDataSetSerializer(serializers.Serializer):
    is_train = serializers.BooleanField()

class ReportsSerializer(serializers.ModelSerializer):

    accuracy = serializers.FloatField()
    f1_score = serializers.FloatField()
    precision = serializers.FloatField()
    recall = serializers.FloatField()

    class Meta:
        model = Reports
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Multiply the fields by 100
        representation["accuracy"] *= 100
        representation["f1_score"] *= 100
        representation["precision"] *= 100
        representation["recall"] *= 100
        # Round the fields to two decimal places
        representation["accuracy"] = round(representation["accuracy"], 2)
        representation["f1_score"] = round(representation["f1_score"], 2)
        representation["precision"] = round(representation["precision"], 2)
        representation["recall"] = round(representation["recall"], 2)
        return representation


class MedicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields = ["medicine_name", "instruction"]


class TrainingDataSetSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source="get_sex_display")
    cp = serializers.CharField(source="get_cp_display")
    slope = serializers.CharField(source="get_slope_display")
    thal = serializers.CharField(source="get_thal_display")
    medicine_id = MedicinesSerializer()

    class Meta:
        model = TrainingDataSet
        fields = "__all__"


class TestingDataSetSerializer(serializers.ModelSerializer):
    training_data = TrainingDataSetSerializer(source="training_id")

    class Meta:
        model = TestingDataSet
        fields = ["training_data", "predicted_values"]


class PatientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patients
        fields = "__all__"
