from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),  # Create this view and template
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('like_item/<int:item_id>/', views.like_item, name='like_item'),
    path('search/', views.search_items, name='search_items'),
    path('adjust_cart/<int:item_id>/', views.adjust_cart, name='adjust_cart'),
    path('thank_you/', views.thank_you, name='thank_you'),
]
