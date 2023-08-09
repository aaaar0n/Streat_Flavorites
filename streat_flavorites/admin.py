from django.contrib import admin
from .models import Category, Subcategory, Item
from .forms import ItemForm

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item, ItemAdmin)