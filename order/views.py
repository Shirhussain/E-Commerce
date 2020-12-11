from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.crypto import get_random_string

from .models import ShopCard, Order, OrderProduct
from .forms import ShopCardForm, OrderForm
from product.models import Category, Product, Variants
from user.models import Profile

def index(request):
    return HttpResponse("order index")

@login_required
def add_to_card(request, id):
    # return HttpResponse(str(id))
    url = request.META.get('HTTP_REFERER') # get the last url 
    current_user = request.user # access to User session information 
    
    # the commented code was for before variant implementation
    # checkproduct = ShopCard.objects.filter(product_id=id) # check product in shop cart
    # if checkproduct:
    #     control = 1 # The product is in the cart
    # else:
    #     control = 0 # the product is not in the cart
    
    product= Product.objects.get(pk=id)
    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCard.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCard.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    # if request.method == 'POST':
    #     form = ShopCardForm(request.POST)
    #     # although by default we have the name of user, so it should be editable because maybe he/she
    #     # would buy for his relative. so they need to edit the name and address.
    #     if form.is_valid():
    #         if control == 1: # update the shop cart
    #             data = ShopCard.objects.get(product_id=id)
    #             data.quantity += form.cleaned_data['quantity']
    #             data.save()
    #         else: # insert to shop cart
    #             data = ShopCard()
    #             data.user_id = current_user.id 
    #             data.product_id = id 
    #             data.quantity = form.cleaned_data['quantity']
    #             data.save()
    #     messages.success(request, "Product successfully added to cart ")
    #     return HttpResponseRedirect(url)


    if request.method == 'POST':  # if there is a post
        form = ShopCardForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCard.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCard.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCard()
                data.user_id = current_user.id
                data.product_id =id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)



    # The following else is come form just one product which means that 
    # it only come from home which you can't add many quantity at once
    # else:
    #     if control == 1: # update shopcart 
    #         data = ShopCard.objects.get(product_id = id)
    #         data.quantity += 1 
    #         data.save()
    #     else: # insert to shop cart at the first time
    #         data = ShopCard()
    #         data.user_id = current_user.id 
    #         data.product_id = id 
    #         data.quantity = 1 
    #         data.save()
    #     messages.success(request, "product aded to shop cart")
    #     return HttpResponseRedirect(url)


    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCard.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCard()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
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

@login_required
def delete_from_card(request, id):
    ShopCard.objects.filter(id= id).delete()
    messages.success(request, "you have been deleted successfully product item from card")
    return HttpResponseRedirect(reverse('order:shop-card'))


def order_product(request):
    category = Category.objects.all()
    current_user = request.user
    shop_card = ShopCard.objects.filter(user_id=current_user.id)

    total = 0
    for rs in shop_card:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity


    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #

            # Move shopcart Item to Order product item
            # shop_card = ShopCard.objects.filter(user_id = request.user.id)
            for rs in shop_card:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                if rs.product.variant == 'None':
                    detail.price    = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id   = rs.variant_id
                detail.amount        = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if  rs.product.variant=='None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.product_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                #************ <> *****************

            ShopCard.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode,'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form= OrderForm()
    profile = Profile.objects.get(user_id=current_user.id)
    context = {'shop_card': shop_card,
                'category': category,
                'total': total,
                'form': form,
                'profile': profile,
            }
    return render(request, 'Order_Form.html', context)


# def order_product(request):
#     category = Category.objects.all()
#     shop_card = ShopCard.objects.filter(user_id = request.user.id)
#     profile = Profile.objects.get(user_id = request.user.id)
#     total = 0 
#     for rs in shop_card:
#         total += rs.product.price*rs.quantity

#     if request.method == "POST":
#         form = OrderForm(request.POST or None)
#         if form.is_valid():
#             # Here gos to Bank process, Send credit cart to bank and get result of payment info
#             # but here in this project i don't have her 
#             # ................................... bank ............ code ......
#             data = Order()
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.address = form.cleaned_data['address']
#             data.city = form.cleaned_data['city']
#             data.phone = form.cleaned_data['phone']
#             data.user_id = request.user.id 
#             data.total = total
#             data.ip = request.META.get('REMOTE_ADDR')
#             ordercode = get_random_string(5).upper()
#             data.code = ordercode
#             data.save()

#             # Move shopcart Item to Order product item
#             # shop_card = ShopCard.objects.filter(user_id = request.user.id)
#             for rs in shop_card:
#                 detail = OrderProduct()
#                 detail.order_id = data.id 
#                 detail.product_id = rs.product_id
#                 detail.user_id = request.user.id
#                 detail.quantity = rs.quantity 
#                 detail.price = rs.product.price 
#                 detail.amount = rs.amount
#                 detail.save()
#                 # Reduce quantity of sold product form Amount of Product
#                 product = Product.objects.get(id=rs.product_id)
#                 product.amount -= rs.quantity 
#                 product.save()
            
#             # Clear and delete Shop Card 
#             ShopCard.objects.filter(user_id = request.user.id)
#             request.session['card_items'] = 0 
#             messages.success(request, "your has been completed successfully, Tank you ")
#             return render(request, "order_complete.html", {'ordercode': ordercode, 'category': category})
#         else:
#             messages.warning(request, form.errors)
#             return HttpResponseRedirect(reverse("order:order-product"))
    
#     form = OrderForm()
#     context = {
#         'category': category,
#         'profile': profile,
#         'total': total,
#         'shop_card': shop_card,
#         'form': form
#     }
#     return render(request, "order_product.html", context)


