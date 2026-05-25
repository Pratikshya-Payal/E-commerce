from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('verify/', views.verify_otp, name='verify'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('profile/info/', views.profile_info, name='profile_info'),
    path('profile/orders/', views.orders, name='orders'),
    path('profile/wishlist/', views.wishlist, name='wishlist'),
    path('profile/coupons/', views.coupons, name='coupons'),
    path('profile/addresses/', views.addresses, name='addresses'),
    path('profile/giftcards/', views.giftcards, name='giftcards'),
    path('profile/notifications/', views.notifications, name='notifications'),
    path('more/', views.more, name='more'),
    path('seller/', views.seller, name='seller'),
    path('notification-settings/', views.notification_settings, name='notification_settings'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    # Simple JSON APIs
    path('api/products/', views.api_products, name='api_products'),
    path('api/orders/', views.api_orders, name='api_orders'),
]
    

