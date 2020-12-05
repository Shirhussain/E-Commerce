from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
import json 

from . models import Settings, ContactMessage
from product.models import Category, Product
from . forms import ContactForm, SearchForm


def index(request):
    setting = Settings.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4] #first 4 product 
    products_latest = Product.objects.all().order_by('-id')[:4] # latest
    products_picked = Product.objects.all().order_by('?')[:4] # random 

    page = "index"

    context = {
        'setting': setting,
        'page': page,
        'category': category,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
    }
    return render(request,'index.html',context)


def about_us(request):
    setting = Settings.objects.get(pk=1)
    context = {
        'setting': setting
    }
    return render(request, 'about.html', context)

def contact_us(request):
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

    setting = Settings.objects.get(pk=1)
    form = ContactForm()
    context = {
        'setting': setting,
        'form': form
    }
    return render(request, 'contact.html', context)

def category_product(request, id, slug):
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()

    context = {
        'products': products,
        'category': category
    }
    return render(request, "category_products.html", context)


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