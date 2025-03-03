# custom_admin/views/analytics.py

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta, date
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from store.models import Product, Category, CartItem
from custom_admin.views.dashboard import is_admin
import random  # For demo data, remove in production

@user_passes_test(is_admin, login_url='admin_login')
def overview(request):
    return render(request, 'custom_admin/analytics/overview.html')

@user_passes_test(is_admin, login_url='admin_login')
def sales_chart(request):
    return render(request, 'custom_admin/analytics/sales_chart.html')

@user_passes_test(is_admin, login_url='admin_login')
def product_analytics(request):
    return render(request, 'custom_admin/analytics/product_analytics.html')

@user_passes_test(is_admin, login_url='admin_login')
def customer_analytics(request):
    return render(request, 'custom_admin/analytics/customer_analytics.html')

@user_passes_test(is_admin, login_url='admin_login')
def chart_data_api(request):
    """API endpoint to provide chart data"""
    chart_type = request.GET.get('type', '')
    period = request.GET.get('period', 'monthly')
    
    if chart_type == 'sales':
        # For demo purposes - replace with actual sales data in production
        today = timezone.now().date()
        
        if period == 'daily':
            days = 30
            labels = [(today - timedelta(days=i)).strftime('%b %d') for i in range(days-1, -1, -1)]
            values = [random.randint(500, 5000) for _ in range(days)]
        elif period == 'weekly':
            weeks = 12
            labels = [f"Week {(today - timedelta(days=i*7)).strftime('%W')}" for i in range(weeks-1, -1, -1)]
            values = [random.randint(3000, 20000) for _ in range(weeks)]
        else:  # monthly
            months = 12
            labels = []
            for i in range(months-1, -1, -1):
                month_date = today.replace(day=1) - timedelta(days=i*30)
                labels.append(month_date.strftime('%b %Y'))
            values = [random.randint(15000, 80000) for _ in range(months)]
        
        return JsonResponse({
            'labels': labels,
            'values': values
        })
    
    elif chart_type == 'categories':
        # Get product count by category
        categories = Category.objects.annotate(product_count=Count('product'))
        labels = [category.name for category in categories]
        values = [category.product_count for category in categories]
        
        return JsonResponse({
            'labels': labels,
            'values': values
        })
    
    elif chart_type == 'popular_products':
        # Get most popular products based on cart items
        products = Product.objects.annotate(
            cart_count=Count('cartitem')
        ).order_by('-cart_count')[:10]
        
        labels = [product.name for product in products]
        values = [product.cart_count for product in products]
        
        return JsonResponse({
            'labels': labels,
            'values': values
        })
    
    elif chart_type == 'stock_levels':
        # Get stock levels for products
        products = Product.objects.order_by('-stock')[:20]
        labels = [product.name for product in products]
        values = [product.stock for product in products]
        
        return JsonResponse({
            'labels': labels,
            'values': values
        })
    
    return JsonResponse({'error': 'Invalid chart type'}, status=400)

