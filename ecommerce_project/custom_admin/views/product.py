from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from store.models import Product, Category
from custom_admin.views.dashboard import is_admin
from django import forms
from django.utils.text import slugify

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image', 'stock', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

@user_passes_test(is_admin, login_url='admin_login')
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Category filter
    category_id = request.GET.get('category', '')
    if category_id and category_id.isdigit():
        products = products.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'custom_admin/products/list.html', {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
    })

@user_passes_test(is_admin, login_url='admin_login')
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Generate slug from name if not provided
            if not product.slug:
                product.slug = slugify(product.name)
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    return render(request, 'custom_admin/products/form.html', {
        'form': form,
        'title': 'Add Product',
        'is_add': True,
    })

@user_passes_test(is_admin, login_url='admin_login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'custom_admin/products/form.html', {
        'form': form,
        'product': product,
        'title': 'Edit Product',
        'is_add': False,
    })

@user_passes_test(is_admin, login_url='admin_login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('admin_products')
    
    return render(request, 'custom_admin/products/delete.html', {
        'product': product,
    })
