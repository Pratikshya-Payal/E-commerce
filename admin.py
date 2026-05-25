from django.contrib import admin
from .models import Profile, Product, Address, Order, WishlistItem, Coupon, Notification

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(WishlistItem)
admin.site.register(Coupon)
admin.site.register(Notification)
