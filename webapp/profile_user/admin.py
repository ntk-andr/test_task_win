from .models import Profile, Barcode

from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']


class BarcodeAdmin(admin.ModelAdmin):
    list_display = ['type', 'data', 'quality']
