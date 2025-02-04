"""
Definition of urls for app.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app.views import TemplateView
from app.views import Helpers
from app.api import *
from django.conf.urls.static import static
from . import settings
from .api import UpdatePrescription, PatientPrescription, CreateAccount

templates = TemplateView()
helpers = Helpers()


# Use Dash for API
api_urls = [
    path(
        "api/get-cardiologists/", CardioInfo.as_view(), name="get-cardiologists"
    ),
    path(
        "api/create-account/", CreateAccount.as_view(), name="create-account"
    ),
    path(
        "api/get-patient-records/", PatientPrescription.as_view(), name="get-patients"
    ),
    path("api/get-prescription/", GetPrescription.as_view(), name="get-prescription"),
    path(
        "api/set-prescription/<int:pk>/",
        UpdatePrescription.as_view(),
        name="set-prescription",
    ),
    path("api/get-datasets-heart/", GetDataSets.as_view(), name="get-datasets"),
    path("api/get-testing/", GetTestingDataset.as_view(), name="get-datasets"),
    path("api/get-reports/", GetEvaluations.as_view(), name="get-evaluations"),
    path("api/add-patients/", AddPatients.as_view(), name="add-patients"),
    path("api/get-prediction/", DiagnoseDisease.as_view(), name="get-prediction"),
    path(
        "api/train-heart-dataset/",
        TrainHeartDataSet.as_view(),
        name="train-heart-dataset",
    ),
    path(
        "api/generate-dataset/",
        GenerateRandomDataSet.as_view(),
        name="generate-dataset",
    ),
]

# Use Underscore for Templates
template_urls = [
    path("accounts/", templates.accounts, name="accounts"),
    path("login/", templates.login, name="login"),
    path("login_user/", helpers.login_user, name="login_user"),
    path("logout/", templates.signout, name="logout"),
    path("", templates.home, name="home"),
    path("add_patients/", templates.add_patients, name="add_patients"),
    path("diagnose/", templates.diagnose, name="diagnose"),
    path("records/", templates.records, name="records"),
    path("dataset/", templates.datasets, name="dataset"),
    path("prescription/<int:id>/", templates.prescription, name="prescription"),
    path("admin/", admin.site.urls),
]

urlpatterns = (
    api_urls
    + template_urls
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
