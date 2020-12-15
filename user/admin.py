from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'language', 'address', 'phone', 'country', 'city', 'image_tag']


admin.site.register(Profile, ProfileAdmin)
