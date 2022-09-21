from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


# Create your views here.


def RegisterAccount(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password2")
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    context = {"registration_form": form}

    return render(request, "registration/signup.html", context)
