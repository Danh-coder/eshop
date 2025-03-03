from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from store.models import Product, Category, Comment, CartItem

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'custom_admin/login.html', {
                'error_message': 'Invalid username or password, or insufficient permissions.'
            })
    
    return render(request, 'custom_admin/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@user_passes_test(is_admin, login_url='admin_login')
def index(request):
    # Get counts for dashboard
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    
    # Get recent products
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    # Get popular products (based on cart items)
    popular_products = Product.objects.annotate(
        cart_count=Count('cartitem')
    ).order_by('-cart_count')[:5]
    
    # Get recent comments
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    return render(request, 'custom_admin/dashboard.html', {
        'total_products': total_products,
        'total_categories': total_categories,
        'recent_products': recent_products,
        'popular_products': popular_products,
        'recent_comments': recent_comments,
    })
