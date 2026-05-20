from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
 
urlpatterns = [
 
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
 
    # Parts
    path('parts/', views.part_list, name='part-list'),
    path('parts/add/', views.part_add, name='part-add'),
    path('parts/<int:pk>/edit/', views.part_edit, name='part-edit'),
    path('parts/<int:pk>/delete/', views.part_delete, name='part-delete'),
 
    # Categories
    path('categories/', views.category_list, name='category-list'),
    path('categories/add/', views.category_add, name='category-add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category-edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
 
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier-list'),
    path('suppliers/add/', views.supplier_add, name='supplier-add'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier-edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier-delete'),
 
    # Transactions
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/add/', views.transaction_add, name='transaction-add'),
 
]
 