from django.urls import path
from custom_admin.views import dashboard, product, category, user, order, analytics

urlpatterns = [
    path('', dashboard.index, name='admin_dashboard'),
    path('login/', dashboard.admin_login, name='admin_login'),
    path('logout/', dashboard.admin_logout, name='admin_logout'),
    
    # Products
    path('products/', product.product_list, name='admin_products'),
    path('products/add/', product.product_add, name='admin_product_add'),
    path('products/<int:pk>/edit/', product.product_edit, name='admin_product_edit'),
    path('products/<int:pk>/delete/', product.product_delete, name='admin_product_delete'),
    
    # Categories
    path('categories/', category.category_list, name='admin_categories'),
    path('categories/add/', category.category_add, name='admin_category_add'),
    path('categories/<int:pk>/edit/', category.category_edit, name='admin_category_edit'),
    path('categories/<int:pk>/delete/', category.category_delete, name='admin_category_delete'),
    
    # Users
    path('users/', user.user_list, name='admin_users'),
    path('users/add/', user.user_add, name='admin_user_add'),
    path('users/<int:pk>/edit/', user.user_edit, name='admin_user_edit'),
    path('users/<int:pk>/delete/', user.user_delete, name='admin_user_delete'),
    
    # Orders
    path('orders/', order.order_list, name='admin_orders'),
    path('orders/<int:pk>/', order.order_detail, name='admin_order_detail'),
    path('orders/<int:pk>/update/', order.order_update, name='admin_order_update'),
    
    # Analytics & Charts
    path('analytics/', analytics.overview, name='admin_analytics'),
    path('analytics/sales/', analytics.sales_chart, name='admin_sales_chart'),
    path('analytics/products/', analytics.product_analytics, name='admin_product_analytics'),
    path('analytics/customers/', analytics.customer_analytics, name='admin_customer_analytics'),
    path('analytics/api/chart-data/', analytics.chart_data_api, name='admin_chart_data'),
]
