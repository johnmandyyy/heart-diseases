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

class Helpers:

    def __init__(self):
        pass

    def login_user(self, request):
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home URL pattern.

    def userIsLoggedIn(self, request):
        return request.user.is_authenticated


class TemplateView:

    helper = Helpers()

    def signout(self, request):
        logout(request)
        return redirect('/')
    
    def login(self, request):
        """Renders the login page."""
        assert isinstance(request, HttpRequest)
        return render(
            request,
            "app/login.html", {
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
                    "title": "Home Page",
                    "year": datetime.now().year,
                },
        )
        return self.login(request)