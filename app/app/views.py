"""
Definition of views.
"""

# Request
from django.http import HttpRequest, HttpResponse

# Renderers
from django.shortcuts import render

# Autentication
from django.contrib.auth import authenticate, login, logout

# Django Tools
from django.shortcuts import redirect

# Tools
from datetime import datetime

from .algorithm import TreeAlgorithm
from .datagen import DataGenerator
from .models import *
from app.data_access import GetPrescription
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.template.loader import render_to_string

from datetime import datetime
from app.data_access import GetPatient

class Helpers:

    def __init__(self):
        pass

    @csrf_exempt
    def login_user(self, request):
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user is not None and user.is_active == True:
            login(request, user)
            return redirect(
                "home"
            )  # Replace 'home' with the name of your home URL pattern.

        return redirect(
            "home"
        ) 

    def userIsLoggedIn(self, request):
        return request.user.is_authenticated


class TemplateView:

    helper = Helpers()

    def signout(self, request):
        logout(request)
        return redirect("/")

    def accounts(self, request):
        """Renders the login page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            "app/accounts.html",
            {
                "title": "Accounts Page",
                "year": datetime.now().year,
            },
        )

    def login(self, request):
        """Renders the login page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            "app/login.html",
            {
                "title": "Home Page",
                "year": datetime.now().year,
            },
        )

    def datasets(self, request):
        """Renders the home page."""

        assert isinstance(request, HttpRequest)
        if self.helper.userIsLoggedIn(request) == True:
            return render(
                request,
                "app/datasets.html",
                {
                    "title": "Home Page",
                    "year": datetime.now().year,
                },
            )
        return self.login(request)

    def home(self, request):
        """Renders the home page."""
        assert isinstance(request, HttpRequest)
        if self.helper.userIsLoggedIn(request) == True:
            
            return render(
                request,
                "app/dashboard.html",
                {
                    "patient_count": GetPatient().get_patient_count(),
                    "title": "Home Page",
                    "year": datetime.now().year,
                },
            )
        return self.login(request)

    def add_patients(self, request):
        """Add patients."""
        assert isinstance(request, HttpRequest)
        if self.helper.userIsLoggedIn(request) == True:
            return render(
                request,
                "app/add_patients.html",
                {
                    "title": "Add Patients",
                    "year": datetime.now().year,
                },
            )
        return self.login(request)

    def diagnose(self, request):
        """Diagnose patients."""
        assert isinstance(request, HttpRequest)
        if self.helper.userIsLoggedIn(request) == True:
            return render(
                request,
                "app/diagnose.html",
                {
                    "title": "Diagnose Patients",
                    "year": datetime.now().year,
                },
            )
        return self.login(request)

    def prescription(self, request, id):
        """Renders the home page."""
        assert isinstance(request, HttpRequest)
        if self.helper.userIsLoggedIn(request) == True:

            prescription_record = GetPrescription(id).retrieve_prescription_record()

            data = {
                "title": "Prescription",
                "year": datetime.now().year,
            }

            return render(
                request,
                "app/prescription.html",
                prescription_record,
            )

        return self.login(request)

    def records(self, request):
        """Renders the records page."""
        assert isinstance(request, HttpRequest)
        if self.helper.userIsLoggedIn(request) == True:

            data = {
                "title": "Prescription",
                "year": datetime.now().year,
            }

            return render(request, "app/records.html", data)

        return self.login(request)
