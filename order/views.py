from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import ShopCard
from .forms import ShopCardForm
from product.models import Category

def index(request):
    return HttpResponse("order is working")

@login_required
def add_to_card(request, id):
    # return HttpResponse(str(id))
    url = request.META.get('HTTP_REFERER') # get the last url 
    current_user = request.user # access to User session information 
    
    checkproduct = ShopCard.objects.filter(product_id=id) # check product in shop cart
    if checkproduct:
        control = 1 # The product is in the cart
    else:
        control = 0 # the product is not in the cart

    if request.method == 'POST':
        form = ShopCardForm(request.POST)
        if form.is_valid():
            if control == 1: # update the shop cart
                data = ShopCard.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else: # insert to shop cart
                data = ShopCard()
                data.user_id = current_user.id 
                data.product_id = id 
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product successfully added to cart ")
        return HttpResponseRedirect(url)

    # The following else is come form just one product which means that 
    # it only come from home which you can't add many quantity at once
    else:
        if control == 1: # update shopcart 
            data = ShopCard.objects.get(product_id = id)
            data.quantity += 1 
            data.save()
        else: # insert to shop cart at the first time
            data = ShopCard()
            data.user_id = current_user.id 
            data.product_id = id 
            data.quantity = 1 
            data.save()
        messages.success(request, "product aded to shop cart")
        return HttpResponseRedirect(url)

def shop_card(request):
    category = Category.objects.all()
    shop_card = ShopCard.objects.filter(user_id = request.user.id)
    total = 0 
    for rs in shop_card:
        total += rs.product.price*rs.quantity
    # return HttpResponse(str(total))
    context = {
        'category': category,
        'shop_card': shop_card,
        'total': total
    }

    return render(request, "shop_card_product.html", context)

def delete_from_card(request, id):
    ShopCard.objects.filter(id= id).delete()
    messages.success(request, "you have been deleted successfully product item from card")
    return HttpResponseRedirect(reverse('order:shop-card'))




