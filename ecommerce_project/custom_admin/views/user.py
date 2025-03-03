from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from custom_admin.views.dashboard import is_admin
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

@user_passes_test(is_admin, login_url='admin_login')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(username__icontains=search_query) | \
                users.filter(email__icontains=search_query) | \
                users.filter(first_name__icontains=search_query) | \
                users.filter(last_name__icontains=search_query)
    
    # Filter by staff status
    staff_filter = request.GET.get('staff', '')
    if staff_filter == 'staff':
        users = users.filter(is_staff=True)
    elif staff_filter == 'customers':
        users = users.filter(is_staff=False)
    
    # Pagination
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'custom_admin/users/list.html', {
        'users': page_obj,
        'search_query': search_query,
        'staff_filter': staff_filter,
    })

@user_passes_test(is_admin, login_url='admin_login')
def user_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('admin_users')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'custom_admin/users/form.html', {
        'form': form,
        'title': 'Add User',
        'is_add': True,
    })

@user_passes_test(is_admin, login_url='admin_login')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user.username}" updated successfully.')
            return redirect('admin_users')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'custom_admin/users/form.html', {
        'form': form,
        'user_obj': user,
        'title': 'Edit User',
        'is_add': False,
    })

@user_passes_test(is_admin, login_url='admin_login')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully.')
        return redirect('admin_users')
    
    return render(request, 'custom_admin/users/delete.html', {
        'user_obj': user,
    })
