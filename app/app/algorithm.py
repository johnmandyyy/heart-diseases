from .models import *
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from .datagen import DataGenerator
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)
from django.db import connection


class TreeAlgorithm:

    DataGen = DataGenerator()

    def __init__(self):
        pass

    def evaluateMetrics(self, y_test, y_pred_test):
        """
        Get precision, recall,
        accuraccy and f1 score.
        """
        cm = confusion_matrix(y_test, y_pred_test)
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Reds)
        plt.title("Confusion matrix")
        plt.colorbar()
        classes = ["Normal", "Abnormal"]  # Assuming binary classification
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)
        fmt = "d"
        thresh = cm.max() / 2.0

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(
                    j,
                    i,
                    format(cm[i, j], fmt),
                    horizontalalignment="center",
                    color="black" if cm[i, j] > thresh else "black",
                )

        plt.ylabel("True Answer")
        plt.xlabel("Predicted Answer")
        plt.tight_layout()
        #plt.show()

        accuracy = accuracy_score(y_test, y_pred_test)
        precision = precision_score(y_test, y_pred_test)
        recall = recall_score(y_test, y_pred_test)
        f1 = f1_score(y_test, y_pred_test)

        if len(Reports.objects.all()) < 1:
            Reports.objects.create(
                accuracy=accuracy, precision=precision, recall=recall, f1_score=f1
            )
        else:
            for report in Reports.objects.all():
                report.accuracy = accuracy
                report.precision = precision
                report.recall = recall
                report.f1_score = f1
                report.save()  # This will ensure that the rounding logic is applied
                break

    def adaBoost(self):

        data = self.DataGen.getDatasets()

        independent_var = []
        correct_answer = []

        for item in data:
            independent_var.append(
                [
                    item["id"],
                    item["sex"],
                    item["age"],
                    item["cp"],
                    item["trestbps"],
                    item["chol"],
                    item["fbs"],
                    item["thalach"],
                    item["exang"],
                    item["oldpeak"],
                    item["slope"],
                    item["ca"],
                    item["thal"],
                    item["is_healed"],
                ]
            )
            correct_answer.append(item["target"])

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            independent_var, correct_answer, test_size=0.2, random_state=42
        )

        # To retain the primary key.
        X_test_original = [row[:] for row in X_test]
        X_train_original = [row[:] for row in X_train]

        # Print X_test_original before modification
        for each_rows in X_test_original:
            print(each_rows)

        # Modify the copied lists (removing the first element)
        for each_rows in X_test:
            each_rows.pop(0)

        for each_rows in X_train:
            each_rows.pop(0)

        # Initialize Decision Tree classifier
        dt_classifier = DecisionTreeClassifier(max_depth=5, random_state=42)

        # Initialize AdaBoost classifier with Decision Tree as base estimator
        adaboost = AdaBoostClassifier(
            base_estimator=dt_classifier, n_estimators=50, random_state=42
        )

        # Train the AdaBoost classifier
        adaboost.fit(X_train, y_train)

        # Predictions
        y_pred_train = adaboost.predict(X_train)
        y_pred_test = adaboost.predict(X_test)

        # Evaluate accuracy
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)

        print("Train Accuracy Abnormal/Normal:", train_accuracy)
        print("Test Accuracy Abnormal/Normal:", test_accuracy)


        TestingDataSet.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='app_testingdataset';")

        for i in range(len(y_test)):
            TestingDataSet.objects.create(
                training_id = TrainingDataSet.objects.get(id = X_train_original[i][0]),
                predicted_values  = y_pred_test[i]
            )
            print(
                f"Primary Key: {X_test_original[i][0]} Sample {i+1}: Predicted: {y_pred_test[i]}, Actual: {y_test[i]}"
            )

        self.evaluateMetrics(y_test, y_pred_test)

    def adaBoostMedicine(self):
        data = self.DataGen.getDatasets()
        X = []
        y = []

        for item in data:

            if item["medicine_id"] == None:
                continue

            X.append(
                [
                    item["sex"],
                    item["age"],
                    item["cp"],
                    item["trestbps"],
                    item["chol"],
                    item["fbs"],
                    item["thalach"],
                    item["exang"],
                    item["oldpeak"],
                    item["slope"],
                    item["ca"],
                    item["thal"],
                ]
            )
            y.append(item["medicine_id"])

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=1
        )

        # Initialize Decision Tree classifier
        dt_classifier = DecisionTreeClassifier(max_depth=3, random_state=1)

        # Initialize AdaBoost classifier with Decision Tree as base estimator
        adaboost = AdaBoostClassifier(
            base_estimator=dt_classifier, n_estimators=3, random_state=1
        )

        # Train the AdaBoost classifier
        adaboost.fit(X_train, y_train)

        # Predictions
        y_pred_train = adaboost.predict(X_train)
        y_pred_test = adaboost.predict(X_test)

        # Evaluate accuracy
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)

        print("Train Accuracy Medicine:", train_accuracy)
        print("Test Accuracy Medicine:", test_accuracy)
