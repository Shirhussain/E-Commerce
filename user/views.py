from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from product.models import Category, Comment
from order.models import Order, OrderProduct 
from .models import Profile
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm


@login_required
def index(request):
    # if you want to don't repeat Category in your functions so use custom template tags
    categoy = Category.objects.all()
    profile = Profile.objects.get(user_id = request.user.id)
    context = {
        'category': categoy,
        'profile': profile
    }
    return render(request, "user_profile.html", context)

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

@login_required
def user_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user) # request user is user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "your account has been updated")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, "user_update.html", context)

@login_required
def user_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "your password has been changed successfully")
            return HttpResponseRedirect(reverse("user:profile"))
        else:
            messages.error(request, "Please correct the error below.<br>"+str(form.errors))
            return HttpResponseRedirect(reverse("user:password"))
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'category': category,
            'form': form
        }
        return render(request, "user_password.html", context)

@login_required
def user_order(request):
    category = Category.objects.all()
    orders = Order.objects.filter(user_id = request.user.id)

    context = {
        'category': category,
        'orders': orders
    }
    return render(request, "user_orders.html", context)

@login_required
def user_order_detail(request, id):
    category = Category.objects.all()
    # why i'm using user_id ---> it's because of security it means that no buddy can access except user
    order = Order.objects.get(user_id = request.user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id = id)
    context = {
        'order': order,
        'orderitems': orderitems,
        'category': category
    }
    return render(request, "user_order_detail.html", context)
    
@login_required
def user_order_product(request):
    category = Category.objects.all()
    order_product = OrderProduct.objects.filter(user_id = request.user.id)
    context = {
        'category': category,
        'order_product': order_product
    }
    return render(request, "order_products.html", context)

@login_required
def user_order_product_detail(request, id, oid):
    category = Category.objects.all()
    order = Order.objects.get(user_id = request.user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=request.user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems
    }
    return render(request, "user_order_detail.html", context)

@login_required
def user_comment(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id = current_user.id)
    context = {
        'category': category,
        'comments': comments
    }
    return render(request, "user_comment.html", context)

@login_required
def user_comment_delete(request, id):
    Comment.objects.filter(id=id, user_id=request.user.id).delete()
    messages.success(request, "Your comment has been deleted successfully!")
    return HttpResponseRedirect(reverse('user:user-comment'))
    

