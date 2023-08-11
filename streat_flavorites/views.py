from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory, Item, Banner
from .models import Cart, CartItem
from random import sample
from django.http import JsonResponse

def index(request):
    categories = Category.objects.all()
    banners = Banner.objects.all()
    top_liked_items = Item.objects.order_by('-likes')[:6]
    context_dict = {'categories': categories, 'top_liked_items': top_liked_items, 'banners': banners}

    return render(request, 'index.html', context_dict)

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    subcategories = category.subcategory_set.all()
    items = Item.objects.filter(subcategory__category=category)  # Filter items based on the category
    categories = Category.objects.all()
    context_dict = {'category': category, 'subcategories': subcategories, 'items': items, 'categories': categories}

    return render(request, 'category_detail.html', context_dict)

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    items = Item.objects.filter(subcategory=subcategory)
    categories = Category.objects.all()
    context_dict = {'subcategory': subcategory, 'items': items, 'categories': categories}

    return render(request, 'subcategory_detail.html', context_dict)

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    categories = Category.objects.all()
    recommended_items = Item.objects.filter(subcategory=item.subcategory).exclude(id=item_id).order_by('?')[:5]
    context_dict = {'item': item, 'categories': categories, 'recommended_items': recommended_items}

    return render(request, 'item_detail.html', context_dict)

def cart(request):
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()

    total_items = sum(item.quantity for item in cart_items)
    
    # Calculate total price and total for each item
    total_price = 0
    for item in cart_items:
        item.total = item.item.price * item.quantity
        total_price += item.total

    total_price = sum(item.item.price * item.quantity for item in cart_items)
    total_weight = sum(item.item.weight * item.quantity for item in cart_items)
    random_items = Item.objects.order_by('?')[:6]
    
    categories = Category.objects.all()
    context_dict = {'cart_items': cart_items, 
                    'total_items': total_items, 
                    'total_price': total_price, 
                    'categories': categories, 
                    'total_weight': total_weight, 
                    'random_items': random_items}

    return render(request, 'cart.html', context_dict)


def add_to_cart(request, item_id):
    
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    else:
        quantity = 1  # Default to 1 if quantity is not provided in POST data

    # Get or create the user's cart
    user_cart, created = Cart.objects.get_or_create(user=request.user)  # Using "_" to indicate that "created" is not used
    
    # Check if the item is already in the cart, increment quantity if so
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, item=item)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity  # Set the initial quantity if the item was just created
    cart_item.save()
    

    return redirect('cart')  # Redirect to the cart page

def adjust_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0 and quantity <= cart_item.item.stocks:
            cart_item.quantity = quantity
            cart_item.save()
    
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    
    return redirect('cart')  # Redirect back to the cart page

def search_items(request):
    random_items = Item.objects.order_by('?')[:12]
    categories = Category.objects.all()
    query = request.GET.get('query')
    if query:
        items = Item.objects.filter(name__icontains=query)
    else:
        items = []

    context_dict = {'query': query, 'items': items, 'categories': categories, 'random_items': random_items}
    return render(request, 'search_results.html', context_dict)

def checkout(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # Process the checkout here (e.g., payment processing)
        # Once the checkout is successful, clear the user's cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart.cartitem_set.all().delete()
        
        # Redirect to the order confirmation page or another relevant page
        return redirect('order_confirmation')  # You can create an 'order_confirmation' URL pattern
        
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    context_dict = {'cart_items': cart_items, 'categories': categories}
    return render(request, 'checkout.html', context_dict)

def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def like_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.likes += 1
    item.save()

    return JsonResponse({'likes': item.likes})