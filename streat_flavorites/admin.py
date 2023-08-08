from django.contrib import admin
from .models import Category, Subcategory, Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stocks', 'subcategory', 'photo')

admin.site.register(Category)
admin.site.register(Subcategory)