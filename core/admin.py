from django.contrib import admin

# Register your models here.
from .models import LostItem, FoundItem

admin.site.register(LostItem)
admin.site.register(FoundItem)
