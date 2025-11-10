"""URL configuration for the store app."""
from django.urls import path

from . import views

urlpatterns = [
    # Main store views
    path('', views.store, name="store"),
    path('product/<int:product_id>/', views.product_detail, name="product_detail"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    
    # Authentication
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('reset-password/<uuid:token>/', views.reset_password, name="reset_password"),
    
    # Reviews
    path('product/<int:product_id>/review/', views.add_review, name="add_review"),
    
    # Debug page
    path('debug-auth/', lambda request: render(request, 'store/debug_auth.html'), name="debug_auth"),
    
    # Vendor dashboard
    path('vendor/', views.vendor_dashboard, name="vendor_dashboard"),
    path('vendor/create-store/', views.create_store, name="create_store"),
    path('vendor/add-product/', views.add_product, name="add_product"),
    path('vendor/store/<int:store_id>/', views.store_detail, name="store_detail"),
    path('vendor/store/<int:store_id>/edit/', views.edit_store, name="edit_store"),
    path('vendor/store/<int:store_id>/delete/', views.delete_store, name="delete_store"),
    path('vendor/product/<int:product_id>/edit/', views.edit_product, name="edit_product"),
    path('vendor/product/<int:product_id>/delete/', views.delete_product, name="delete_product"),
    path('vendor/products/', views.manage_products, name="manage_products"),
    path('profile/', views.profile, name="profile"),
]