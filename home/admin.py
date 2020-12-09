from django.contrib import admin
from .models import Settings, ContactMessage, FAQ


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'updated_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'updated_at', 'status']
    readonly_fields = ['name', 'email', 'subject','ip', 'message']
    list_filter = ['status']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber','status']
    list_filter = ['status']

admin.site.register(Settings, SettingsAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)