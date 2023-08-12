from django.contrib import admin
from .models import Category, Subcategory, Item, Banner
from .forms import ItemForm

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ('name', 'id', 'price', 'subcategory', 'get_category', 'likes', 'weight')
    list_filter = ('subcategory__category', 'subcategory')
    search_fields = ('name', 'subcategory__name', 'subcategory__category__name')

    def get_category(self, obj):
        return obj.subcategory.category.name if obj.subcategory else '-'
    get_category.short_description = 'Category'

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Add 'category' to the list_display
    list_select_related = ('category',)  # Optimize database queries


admin.site.register(Category)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Item, ItemAdmin)