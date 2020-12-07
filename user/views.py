from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from product.models import Category
from .models import Profile

def index(request):
    return HttpResponse("Hellow users")


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user_id = request.user.id)
            request.session['userimage'] = profile.image.url
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('home:index'))
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, "your username or password is in correct plz try again")
            return HttpResponseRedirect(reverse('user:login'))

    category = Category.objects.all()

    context = {
        'category': category
    }
    return render(request, "login.html", context)

def signup_form(request):
    if request.method == "POST":
        return HttpResponse(request)

    category = Category.objects.all()

    context = {
        'category': category
    }
    return render(request, "logout.html", context)

def logout_form(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:index"))
