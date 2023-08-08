from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory, Item
from .models import Cart, CartItem
from django.http import JsonResponse

def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    subcategories = category.subcategory_set.all()
    items = Item.objects.filter(subcategory__category=category)  # Filter items based on the category

    return render(request, 'category_detail.html', {'category': category, 'subcategories': subcategories, 'items': items})

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    items = Item.objects.filter(subcategory=subcategory)

    return render(request, 'subcategory_detail.html', {'subcategory': subcategory, 'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    return render(request, 'item_detail.html', {'item': item})

def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    
    total_items = sum(item.quantity for item in cart_items)
    
    # Calculate total price
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_items': total_items, 'total_price': total_price})


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    else:
        quantity = 1

    # Get or create the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)  # Assuming you have authentication
    
    # Check if the item is already in the cart, increment quantity if so
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, item=item)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return redirect('cart')  # Redirect to the cart page

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    
    return redirect('cart')  # Redirect back to the cart page

def checkout(request):
    if request.method == 'POST':
        # Process the checkout here (e.g., payment processing)
        # Once the checkout is successful, clear the user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart.cartitem_set.all().delete()
        
        # Redirect to the order confirmation page or another relevant page
        return redirect('order_confirmation')  # You can create an 'order_confirmation' URL pattern
        
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()

    return render(request, 'checkout.html', {'cart_items': cart_items})

def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def like_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.likes += 1
    item.save()

    return JsonResponse({'likes': item.likes})