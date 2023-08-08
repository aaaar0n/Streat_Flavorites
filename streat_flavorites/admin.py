from django.contrib import admin
from .models import Category, Subcategory, Item

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item)