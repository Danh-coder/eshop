from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from store.models import Order  # Assuming you have an Order model
from custom_admin.views.dashboard import is_admin
from django import forms

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

@user_passes_test(is_admin, login_url='admin_login')
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(id__icontains=search_query) | \
                orders.filter(user__username__icontains=search_query) | \
                orders.filter(user__email__icontains=search_query)
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Date range filter
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    if start_date and end_date:
        orders = orders.filter(created_at__range=[start_date, end_date])
    
    # Pagination
    paginator = Paginator(orders, 20)  # Show 20 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique statuses for filter dropdown
    statuses = Order.objects.values_list('status', flat=True).distinct()
    
    return render(request, 'custom_admin/orders/list.html', {
        'orders': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'start_date': start_date,
        'end_date': end_date,
        'statuses': statuses,
    })

@user_passes_test(is_admin, login_url='admin_login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    return render(request, 'custom_admin/orders/detail.html', {
        'order': order,
    })

@user_passes_test(is_admin, login_url='admin_login')
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order #{order.id} status updated successfully.')
            return redirect('admin_order_detail', pk=order.id)
    else:
        form = OrderStatusForm(instance=order)
    
    return render(request, 'custom_admin/orders/update.html', {
        'form': form,
        'order': order,
    })
