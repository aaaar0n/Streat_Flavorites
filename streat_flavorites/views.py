from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory, Item, Banner
from .models import Cart, CartItem
from random import sample
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import CartItem
from .forms import CheckoutForm
import string
import random

def index(request):
    categories = Category.objects.all()
    banners = Banner.objects.all()
    top_liked_items = Item.objects.order_by('-likes')[:6]

    # Get random items for each subcategory
    subcategory_items = {}
    for category in categories:
        for subcategory in category.subcategory_set.all():
            random_items = list(subcategory.item_set.all().order_by('?')[:6])
            subcategory_items[subcategory] = random_items

    context_dict = {'categories': categories, 'top_liked_items': top_liked_items, 'banners': banners, 'subcategory_items': subcategory_items}

    return render(request, 'index.html', context_dict)


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    subcategories = category.subcategory_set.all()
    items = Item.objects.filter(subcategory__category=category)  # Filter items based on the category
    categories = Category.objects.all()
    random_items = Item.objects.order_by('?')[:12]
    context_dict = {'category': category, 'subcategories': subcategories, 'items': items, 'categories': categories, 'random_items': random_items }

    return render(request, 'category_detail.html', context_dict)

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    items = Item.objects.filter(subcategory=subcategory)
    categories = Category.objects.all()
    random_items = Item.objects.order_by('?')[:12]
    context_dict = {'subcategory': subcategory, 'items': items, 'categories': categories, 'random_items': random_items}
    
    return render(request, 'subcategory_detail.html', context_dict)

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    categories = Category.objects.all()
    recommended_items = Item.objects.filter(subcategory=item.subcategory).exclude(id=item_id).order_by('?')[:12]
    context_dict = {'item': item, 'categories': categories, 'recommended_items': recommended_items}

    return render(request, 'item_detail.html', context_dict)

def cart(request):
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    
    # Calculate total price and total for each item
    total_price = 0
    for item in cart_items:
        item.total = item.item.price * item.quantity  # Calculate item total here
        total_price += item.total

    total_weight = sum(item.item.weight * item.quantity for item in cart_items)
    random_items = Item.objects.order_by('?')[:12]
    
    categories = Category.objects.all()
    context_dict = {'cart_items': cart_items, 
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
    random_items = Item.objects.order_by('?')[:12]
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    
    total_weight = sum(item.item.weight * item.quantity for item in cart_items)


    total_price = 0
    for item in cart_items:
        item.total = item.item.price * item.quantity  # Calculate item total here
        total_price += item.total
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data and send email
            order_details = {
                'user_name': form.cleaned_data['user_name'],
                'user_email': form.cleaned_data['user_email'],
                'contact_number': form.cleaned_data['contact_number'],
                'delivery_address': form.cleaned_data['delivery_address'],
                'total_price': total_price,
                'total_weight': total_weight,
                'cart_items': cart_items,
            }
            
            # Send email
            send_order_email(order_details)
            
            # Clear the cart or mark items as purchased
            user_cart.cartitem_set.all().delete()
            
            # Redirect to the thank you page
            return redirect('thank_you')  # Replace with your desired URL
            
    else:
        form = CheckoutForm()
    
    context = {'form': form, 'cart_items': cart_items, 'total_price': total_price, 'total_weight': total_weight, 'categories': categories, 'random_items': random_items}
    return render(request, 'checkout.html', context)

def send_order_email(order_details):
    reference_code = generate_unique_code()
    subject_admin = f'New Order - REF-ID: {reference_code}'
    message_admin = f'You have received a new order:\n\n' \
              f'Name: {order_details["user_name"]}\n' \
              f'Email: {order_details["user_email"]}\n' \
              f'Contact Number: {order_details["contact_number"]}\n' \
              f'Delivery Address: {order_details["delivery_address"]}\n' \
              f'Total Price: ${order_details["total_price"]}\n' \
              f'Estimated Weight: {order_details["total_weight"]} g\n\n' \
              f'Order Items:\n'
    
    subject_buyer = f'Order Request Successful - REF-ID: {reference_code}'
    message_buyer = f'Here is the summary of your order:\n\n' \
              f'Name: {order_details["user_name"]}\n' \
              f'Email: {order_details["user_email"]}\n' \
              f'Contact Number: {order_details["contact_number"]}\n' \
              f'Delivery Address: {order_details["delivery_address"]}\n' \
              f'Total Price: ${order_details["total_price"]}\n' \
              f'Estimated Weight: {order_details["total_weight"]} g\n\n' \
              f'Order Items:\n'
    
    for item in order_details["cart_items"]:
        message_admin += f'{item.quantity}x {item.item.name} - ${item.total}\n'
        
    message_buyer = message_admin

    admin_email = 'sflavorites.host@gmail.com'  # Change this to your email address
    send_mail(subject_admin, message_admin, 'autoreply.sflavorites@gmail.com', [admin_email])
    send_mail(subject_buyer, message_buyer, 'autoreply.sflavorites@gmail.com', [order_details["user_email"]]) 
    
    
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def thank_you(request):
    return render(request, 'thank_you.html')

def like_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.likes += 1
    item.save()

    return JsonResponse({'likes': item.likes})

def generate_unique_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(10))
    return code