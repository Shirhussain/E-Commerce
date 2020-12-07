from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from product.models import Category
from .models import Profile
from .forms import SignUpForm

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() # signUp completed here but now i'm gonna login at the same time
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # then I need to create a Profile for user as well--> one way is with signal and 
            # another way is as follows 
            data = Profile()
            data.user_id = request.user.id 
            data.image = "profile_image/avatar.png"
            data.save()
            messages.success(request, "your profile has been created successfully")
            return HttpResponseRedirect(reverse("home:index"))
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(reverse("user:signup"))
    form = SignUpForm()
    category = Category.objects.all()

    context = {
        'category': category, 
        'form': form
    }
    return render(request, "signup.html", context)

def logout_form(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:index"))
