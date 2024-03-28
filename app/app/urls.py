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

templates = TemplateView()
helpers = Helpers()


# Use Dash for API
api_urls = [
    path('api/get-datasets-heart/', GetDataSets.as_view(), name='get-datasets'),
    path('api/get-testing/', GetTestingDataset.as_view(), name='get-datasets'),
    path('api/get-reports/', GetEvaluations.as_view(), name='get-evaluations'),
    path('api/add-patients/', AddPatients.as_view(), name='add-patients'),
    path('api/get-prediction/', DiagnoseDisease.as_view(), name='get-prediction')
]

# Use Underscore for Templates
template_urls = [
    path('login/', templates.login, name='login'),

    path('login_user/', helpers.login_user, name='login_user'),
    path('logout/', templates.signout, name='logout'),

    path('', templates.home, name='home'),
    path('add_patients/', templates.add_patients, name='add_patients'),
    path('diagnose/', templates.diagnose, name='diagnose'),
    path('dataset/', templates.datasets, name='dataset'),
    path('admin/', admin.site.urls),
]



urlpatterns = api_urls + template_urls

