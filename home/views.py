import json 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import translation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings

from . models import Settings, ContactMessage, FAQ, SettingLang, Language
from . forms import ContactForm, SearchForm
from product.models import Category, CategoryLang, Comment, Images, Product, Variants
from product.forms import CommentForm
from user.models import Profile


def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
        #return HttpResponse(lang)
        return HttpResponseRedirect(lang)

def index(request):
    # check currency, set currency 
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    setting = Settings.objects.get(pk=1)
    # category = Category.objects.all()
    products_latest = Product.objects.all().order_by('-id')[:4] # latest
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
        products_latest = Product.objects.raw(
            'SELECT p.id,p.price, l.title, l.description,l.slug  '
            'FROM product_product as p '
            'LEFT JOIN product_productlang as l '
            'ON p.id = l.product_id '
            'WHERE  l.lang=%s ORDER BY p.id DESC LIMIT 4', [currentlang])

    products_slider = Product.objects.all().order_by('id')[:4] #first 4 product 
    products_picked = Product.objects.all().order_by('?')[:4] # random 
    page = "index"
    context = {
        'setting': setting,
        'page': page,
        # 'category': category,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
    }
    return render(request,'index.html',context)

def about_us(request):
    # category = Category.objects.all()
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Settings.objects.get(pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
    context = {
        'setting': setting,
        # 'category': category
    }
    return render(request, 'about.html', context)

def contact_us(request):
    currentlang = request.LANGUAGE_CODE[0:2]
    # category = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "your message has been submitted we will get you back soon ")
            return redirect('home:contact-us')
            # return HttpResponseRedirect(reverse('home:contact-us'))

    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Settings.objects.get(pk=1)
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
    form = ContactForm()
    context = {
        'setting': setting,
        'form': form,
        # 'category': category
    }
    return render(request, 'contact.html', context)

# this one was for before multi language implementation 
# def category_product(request, id, slug):
#     products = Product.objects.filter(category_id=id)
#     category = Category.objects.all()

#     context = {
#         'products': products,
#         'category': category
#     }
#     return render(request, "category_products.html", context)


def category_product(request,id,slug):
    # category = Category.objects.all()
    defaultlang = settings.LANGUAGE_CODE[0:2] # i get first two because it's to lang like --> en-US or fa-IR also in my table i define only 'en' or 'af'
    currentlang = request.LANGUAGE_CODE[0:2]
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id) #default language
    if defaultlang != currentlang:
        try:
            products = Product.objects.raw(
                'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                'FROM product_product as p '
                'LEFT JOIN product_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.category_id=%s and l.lang=%s', [id, currentlang])
        except:
            pass
        catdata = CategoryLang.objects.get(category_id=id, lang=currentlang)

    context={
        'products': products,
        # 'category':category,
        'catdata':catdata }
    return render(request,'category_products.html',context)


def search(request):
    if request.method == 'POST': 
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']

            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {
                'products': products,
                'category': category,
                'query': query
                }
            return render(request, 'search_products.html', context)
    
    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for product in products:
            product_json = {}
            # product_json = product.title + "," + product.description
            product_json = product.title 
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, id, slug):
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2] #en-EN
    currentlang = request.LANGUAGE_CODE[0:2]
    #category = categoryTree(0, '', currentlang)
    # category = Category.objects.all()
    product = Product.objects.get(pk=id)

    if defaultlang != currentlang:
        try:
            prolang =  Product.objects.raw('SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                                            'FROM product_product as p '
                                            'INNER JOIN product_productlang as l '
                                            'ON p.id = l.product_id '
                                            'WHERE p.id=%s and l.lang=%s',[id,currentlang])
            product=prolang[0] # selecting one row because of our detail which is one
        except:
            pass
    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end

    images = Images.objects.filter(product_id = id)
    comments = Comment.objects.filter(product_id = id, status=True)
    # if you don't wanna use 'averagereview or counterreview' of model so you can do in this view as follows
    # review = Comment.objects.filter(product_id=id, status=True).aggregate(Count('id'),Avg('rate'))
    # Retrieve values : review.rate__avg, review.id, status =True).aggregate(Count('id'), Avg('rate'))
    # review = Comment.objects.raw('SELECT id, count(id) as counterew, avg(rate) as avgrew From product_comment WHERE product_id=%s and STATUS = "True"',[id])[0]
    # Retrieve values: review.avgrew, review.countrew
    context = {
        'product': product,
        'images': images, 
        # 'category': category,
        'comments': comments
    }
    if product.variant != "None":
        if request.method == "POST":
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) # select product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title+' Size:'+str(variant.size)+' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'query': query
        })
    return render(request, "product_detail.html", context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action')=='post':
        size_id = request.POST.get('size')
        productid= request.POST.get('productid')
        colors = Variants.objects.filter(product_id =productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def add_comment(request, id):
    url = request.META.get('HTTP_REFERER') # refere to the last or current url
    # some time print is not working so you need to return HttpResponse instead 
    # return HttpResponse(url)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            data.user_id = request.user.id 
            data.save()
            messages.success(request, "your review hass been submitted tnx for your intrest")
            return HttpResponseRedirect(url)
    
    return HttpResponseRedirect(url)


def faq(request):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    if defaultlang==currentlang:
        faq = FAQ.objects.filter(status="True",lang=defaultlang).order_by("ordernumber")
    else:
        faq = FAQ.objects.filter(status="True",lang=currentlang).order_by("ordernumber")

    # category = Category.objects.all() 
    context = {
        'faq': faq,
        # 'category': category
    }
    return render(request, "faq.html", context)

def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)

@login_required
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    language=Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    #Save to User profile database
    data = Profile.objects.get(user_id=curren_user.id )
    data.language_id = language.id
    data.currency_id = request.session['currency']
    data.save()  # save data
    return HttpResponseRedirect(lasturl)