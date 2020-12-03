from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages

from . models import Settings, ContactMessage
from . forms import ContactForm


def index(request):
    setting = Settings.objects.get(pk=1)
    page = "index"

    context = {
        'setting': setting,
        'page': page
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

    setting = Settings.objects.get(pk=1)
    form = ContactForm()
    context = {
        'setting': setting,
        'form': form
    }
    return render(request, 'contact.html', context)