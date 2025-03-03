from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Category, Product, Comment, Cart, CartItem
from .forms import CommentForm, RegisterForm

def home(request):
    featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    return render(request, 'store/home.html', {
        'featured_products': featured_products,
    })

def product_list(request):
    products = Product.objects.filter(available=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Sorting
    sort_option = request.GET.get('sort', '')
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    elif sort_option == 'newest':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/product_list.html', {
        'products': page_obj,
        'search_query': search_query,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    comments = Comment.objects.filter(product=product).order_by('-created_at')
    comment_form = CommentForm()
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'comments': comments,
        'comment_form': comment_form,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products,
    })

@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully.')
        else:
            messages.error(request, 'There was an error with your comment.')
    
    return redirect('product_detail', slug=product.slug)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    
    # Get quantity from form or default to 1
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if product is already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        messages.info(request, f'Updated {product.name} quantity in your cart.')
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        messages.success(request, f'Added {product.name} to your cart.')
    
    # Redirect back to the referring page or product detail
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return HttpResponseRedirect(next_url)
    return redirect('product_detail', slug=product.slug)

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if user has permission to modify this cart item
    if request.user.is_authenticated and cart_item.cart.user != request.user:
        messages.error(request, "You don't have permission to modify this cart.")
        return redirect('cart_detail')
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.info(request, 'Cart updated successfully.')
    else:
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if user has permission to modify this cart item
    if request.user.is_authenticated and cart_item.cart.user != request.user:
        messages.error(request, "You don't have permission to modify this cart.")
        return redirect('cart_detail')
    
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    
    return redirect('cart_detail')

def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    elif request.session.session_key:
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    else:
        # No cart exists yet
        request.session.create()
        cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    
    return render(request, 'store/cart_detail.html', {'cart': cart})
