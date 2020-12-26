from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import User


def index(request):
    return render(request, "generator/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "generator/login.html", {
                "message": "Invalid Username or Password."
            })
    else:
        return render(request, "generator/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
@require_POST
def create_schema(request):
    pass
    
@login_required
def generated_data(request):
    pass

@login_required
def schemas(request, id):
    # todo get schemas get fromd db
    items = []

    return render(request, "generator/schemas.html", {
        "schemas": items,
        })

@require_POST
def generate_fake_data(request, id):
    pass
