import random
from datetime import date

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import MobileForm, OTPForm, ProfileForm
from .models import Product, Order


def sample_products():
    return [
        {
            'name': 'Boho Floral Midi Dress',
            'slug': 'boho-floral-midi-dress',
            'price': 528,
            'old_price': 3399,
            'discount': 84,
            'category': 'Women',
            'material': 'Cotton Blend',
            'availability': 'In Stock',
            'rating': 3.8,
            'review_count': 222,
            'main_image': 'https://images.unsplash.com/photo-1523381212041-58c56f4ec8d4?auto=format&fit=crop&w=800&q=80',
            'image2': 'https://images.unsplash.com/photo-1523381212041-58c56f4ec8d4?auto=format&fit=crop&w=600&q=80',
            'image3': 'https://images.unsplash.com/photo-1520962916339-8589c9f5a17f?auto=format&fit=crop&w=600&q=80',
            'colors': ['Off White', 'Black', 'Green', 'Blue'],
            'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
        },
        {
            'name': 'Realme Wireless Earbuds',
            'slug': 'realme-wireless-earbuds',
            'price': 1499,
            'old_price': 2999,
            'discount': 50,
            'category': 'Electronics',
            'material': 'Plastic',
            'availability': 'Only 15 left',
            'rating': 4.2,
            'review_count': 1320,
            'main_image': 'https://images.unsplash.com/photo-1519666213635-3b789c0a4a70?auto=format&fit=crop&w=800&q=80',
            'image2': 'https://images.unsplash.com/photo-1519666213635-3b789c0a4a70?auto=format&fit=crop&w=600&q=80',
            'image3': 'https://images.unsplash.com/photo-1512314889357-e157c22f938d?auto=format&fit=crop&w=600&q=80',
            'colors': ['Black', 'White', 'Blue'],
            'sizes': ['One Size'],
        },
        {
            'name': 'Warehouse Metal Shoe Rack',
            'slug': 'warehouse-metal-shoe-rack',
            'price': 394,
            'old_price': 799,
            'discount': 51,
            'category': 'Home',
            'material': 'Metal',
            'availability': 'In Stock',
            'rating': 4.5,
            'review_count': 440,
            'main_image': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=800&q=80',
            'image2': 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=600&q=80',
            'image3': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=600&q=80',
            'colors': ['Grey', 'Black'],
            'sizes': ['One Size'],
        },
        {
            'name': 'Men Checkered Casual Shirt',
            'slug': 'men-checkered-casual-shirt',
            'price': 375,
            'old_price': 1899,
            'discount': 80,
            'category': 'Fashion',
            'material': 'Cotton',
            'availability': 'In Stock',
            'rating': 4.0,
            'review_count': 890,
            'main_image': 'https://images.unsplash.com/photo-1520975915854-d9215f47edaf?auto=format&fit=crop&w=800&q=80',
            'image2': 'https://images.unsplash.com/photo-1520975915854-d9215f47edaf?auto=format&fit=crop&w=600&q=80',
            'image3': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=600&q=80',
            'colors': ['Green', 'Blue', 'Black'],
            'sizes': ['S', 'M', 'L', 'XL'],
        },
    ]


def sample_user_profile(user):
    return {
        'first_name': user.first_name or 'Minakshi',
        'last_name': user.last_name or 'Pramanik',
        'gender': 'Female',
        'email': user.email or 'minakshi@example.com',
        'phone': user.profile.phone if hasattr(user, 'profile') else '+919348593886',
    }


def home(request):
    query = request.GET.get('q', '').strip()
    products_qs = Product.objects.all()
    if query:
        products_qs = products_qs.filter(
            Q(name__icontains=query)
            | Q(category__icontains=query)
            | Q(material__icontains=query)
        )
    products = [
        {
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
            'old_price': float(p.old_price) if p.old_price else None,
            'discount': p.discount,
            'category': p.category,
            'material': p.material,
            'main_image': p.image,
            'image2': p.image2,
            'image3': p.image3,
            'colors': [c.strip() for c in p.color_options.split(',')] if p.color_options else [],
            'sizes': [s.strip() for s in p.size_options.split(',')] if p.size_options else [],
            'description': f"{p.name} is a premium {p.category or 'quality'} product made from {p.material or 'fine materials'}. Enjoy {p.discount}% off for a limited time.",
        }
        for p in products_qs
    ]
    context = {
        'page_title': 'My Shop Home',
        'query': query,
        'products': products,
        'latest_items': products[:3],
        'offer_items': products[1:],
    }
    return render(request, 'store/home.html', context)


def signup(request):
    form = MobileForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mobile = form.cleaned_data['mobile'].strip()
        user_exists = User.objects.filter(username=mobile).exists() or User.objects.filter(email=mobile).exists()
        if user_exists:
            messages.warning(request, 'This number/email is already registered. Please sign in instead.')
            return redirect('store:signin')
        code = '%06d' % random.randint(0, 999999)
        request.session['otp_code'] = code
        request.session['pending_mobile'] = mobile
        request.session['pending_action'] = 'signup'
        messages.success(request, f'OTP sent successfully to {mobile}. Use code {code} for demo.')
        return redirect('store:verify')
    return render(request, 'store/auth_signup.html', {'form': form, 'page_title': 'Sign Up'})


def signin(request):
    form = MobileForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mobile = form.cleaned_data['mobile'].strip()
        user_exists = User.objects.filter(username=mobile).exists() or User.objects.filter(email=mobile).exists()
        if not user_exists:
            messages.info(request, 'No account found. Please register first.')
            return redirect('store:signup')
        code = '%06d' % random.randint(0, 999999)
        request.session['otp_code'] = code
        request.session['pending_mobile'] = mobile
        request.session['pending_action'] = 'signin'
        messages.success(request, f'OTP sent successfully to {mobile}. Use code {code} for demo.')
        return redirect('store:verify')
    return render(request, 'store/auth_login.html', {'form': form, 'page_title': 'Login'})


def verify_otp(request):
    form = OTPForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        otp = form.cleaned_data['otp'].strip()
        expected = request.session.get('otp_code')
        if otp == expected:
            mobile = request.session.get('pending_mobile', '')
            action = request.session.get('pending_action')
            if action == 'signup':
                if User.objects.filter(username=mobile).exists() or User.objects.filter(email=mobile).exists():
                    messages.warning(request, 'User already exists, please sign in.')
                    return redirect('store:signin')
                username = mobile
                email = mobile if '@' in mobile else ''
                user = User.objects.create_user(username=username, email=email, password='django1234')
                user.first_name = 'Minakshi'
                user.last_name = 'Pramanik'
                user.save()
                user.profile = None
                user.save()
                login(request, user)
                messages.success(request, 'Verified successfully! Account created.')
                return redirect('store:home')
            if action == 'signin':
                user = User.objects.filter(username=mobile).first() or User.objects.filter(email=mobile).first()
                if user:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('store:home')
                messages.error(request, 'Unable to find your account.')
                return redirect('store:signin')
        messages.error(request, 'Invalid OTP, please try again.')
    return render(request, 'store/auth_verify.html', {'form': form, 'page_title': 'Verify OTP'})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:home')


def get_dashboard_context(user):
    return {
        'profile': sample_user_profile(user),
        'orders': [
            {
                'product': 'ZENVEKYO PP Collapsible Wardrobe',
                'price': 394,
                'status': 'On the way',
                'status_tag': 'delivery expected by May 10',
                'detail': 'Your item has been shipped.',
                'date': '2026-05-02',
            },
            {
                'product': 'Zyra 5 Tier Book Shelf',
                'price': 306,
                'status': 'On the way',
                'status_tag': 'delivery expected by May 14',
                'detail': 'Seller has processed your order.',
                'date': '2026-05-04',
            },
            {
                'product': 'HouseOfCommon Women Fit and Flare Dress',
                'price': 441,
                'status': 'Cancelled',
                'status_tag': 'Cancelled on Feb 06',
                'detail': 'Your order was cancelled as per your request.',
                'date': '2026-02-06',
            },
        ],
        'wishlist': [
            {'title': 'U TURN Men Checkered Casual Green Shirt', 'price': 375, 'status': 'Available'},
            {'title': 'Ethniclook Women Fit and Flare Dress', 'price': None, 'status': 'Currently unavailable'},
            {'title': 'PURVAJA Women Empire Waist Dress', 'price': 396, 'status': 'Available'},
        ],
        'coupons': [
            {'title': 'Get Product at Re.1', 'valid': 'Valid till 31 May, 2026', 'detail': 'Get Product at Re.1 (Valid till: 11:59 PM, 31 May)'},
            {'title': 'Get Product at Re.1', 'valid': 'Valid till 31 May, 2026', 'detail': 'Get Product at Re.1 (Valid till: 11:59 PM, 31 May)'},
        ],
        'addresses': [
            {'label': 'HOME', 'name': 'Pratikshya Pramanik', 'phone': '+91 9348593886', 'street': 'Gita autonomous college Bhubaneswar, Madanpur, Khordha District, Odisha', 'zipcode': '752054'},
            {'label': 'HOME', 'name': 'Minakshi Pramanik', 'phone': '+91 9348593886', 'street': 'Satsulia, Hanuman Temple, Kamarda, Baleshwar District, Odisha', 'zipcode': '756035'},
        ],
        'notifications': [
            {'title': 'All caught up!', 'message': 'There are no new notifications for you.', 'empty': True},
        ],
    }


@login_required(login_url='store:signin')
def profile_dashboard(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'My Profile'})
    return render(request, 'store/dashboard.html', context)


@login_required(login_url='store:signin')
def profile_info(request):
    user = request.user
    initial = sample_user_profile(user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('store:profile_info')
    else:
        form = ProfileForm(initial=initial)
    return render(request, 'store/profile_info.html', {'form': form, 'page_title': 'Profile Information'})


@login_required(login_url='store:signin')
def orders(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'My Orders'})
    return render(request, 'store/orders.html', context)


@login_required(login_url='store:signin')
def wishlist(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'My Wishlist'})
    return render(request, 'store/wishlist.html', context)


@login_required(login_url='store:signin')
def coupons(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'Coupons'})
    return render(request, 'store/coupons.html', context)


@login_required(login_url='store:signin')
def addresses(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'Manage Addresses'})
    return render(request, 'store/addresses.html', context)


@login_required(login_url='store:signin')
def giftcards(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'Gift Cards'})
    return render(request, 'store/giftcards.html', context)


@login_required(login_url='store:signin')
def notifications(request):
    context = get_dashboard_context(request.user)
    context.update({'page_title': 'Notifications'})
    return render(request, 'store/notifications.html', context)


def more(request):
    return render(request, 'store/more.html', {'page_title': 'More'})


def seller(request):
    return render(request, 'store/seller.html', {'page_title': 'Become a Seller'})


def notification_settings(request):
    return render(request, 'store/notification_settings.html', {'page_title': 'Notification Settings'})


def cart(request):
    session_cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for pid, item in session_cart.items():
        cart_items.append(item)
        total += item.get('price', 0) * item.get('qty', 1)
    return render(request, 'store/cart.html', {
        'page_title': 'Cart',
        'cart_items': cart_items,
        'cart_total': total,
    })


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug).first()
    if not product:
        products = sample_products()
        product = next((item for item in products if item['slug'] == slug), products[0])
        return render(request, 'store/product_detail.html', {'product': product, 'page_title': product['name']})
    product_data = {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'price': float(product.price),
        'old_price': float(product.old_price) if product.old_price else None,
        'discount': product.discount,
        'category': product.category,
        'material': product.material,
        'main_image': product.image,
        'image2': product.image2,
        'image3': product.image3,
        'colors': [c.strip() for c in product.color_options.split(',')] if product.color_options else [],
        'sizes': [s.strip() for s in product.size_options.split(',')] if product.size_options else [],
        'description': f"{product.name} is a premium {product.category or 'quality'} product crafted from {product.material or 'best materials'}. It offers excellent comfort, durability, and style for daily use.",
    }
    return render(request, 'store/product_detail.html', {'product': product_data, 'page_title': product.name})


@require_POST
def add_to_cart(request):
    pid = request.POST.get('product_id')
    qty = int(request.POST.get('quantity', 1))
    color = request.POST.get('color', '')
    size = request.POST.get('size', '')
    product = get_object_or_404(Product, pk=pid)
    cart = request.session.get('cart', {})
    item = cart.get(str(product.id), {
        'id': product.id,
        'title': product.name,
        'price': float(product.price),
        'qty': 0,
        'color': color,
        'size': size,
    })
    item['qty'] = item.get('qty', 0) + qty
    cart[str(product.id)] = item
    request.session['cart'] = cart
    return redirect('store:cart')


@login_required(login_url='store:signin')
def checkout(request):
    session_cart = request.session.get('cart', {})
    if not session_cart:
        messages.info(request, 'Your cart is empty.')
        return redirect('store:cart')
    for pid, item in session_cart.items():
        Order.objects.create(
            user=request.user,
            product_name=item.get('title'),
            price=item.get('price'),
            status='pending',
            order_time=date.today(),
            color=item.get('color', ''),
            size=item.get('size', ''),
        )
    request.session['cart'] = {}
    messages.success(request, 'Order placed successfully.')
    return redirect('store:orders')


def api_products(request):
    if request.method == 'GET':
        items = []
        for p in Product.objects.all():
            items.append({'id': p.id, 'name': p.name, 'slug': p.slug, 'price': float(p.price)})
        return JsonResponse({'products': items})
    if request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'permission denied'}, status=403)
        data = request.POST
        p = Product.objects.create(
            name=data.get('name', 'Untitled'),
            slug=data.get('slug', f"product-{random.randint(1000,9999)}"),
            category=data.get('category', ''),
            price=data.get('price', 0),
        )
        return JsonResponse({'created': p.id}, status=201)


def api_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'authentication required'}, status=401)
    if request.method == 'GET':
        items = []
        for o in Order.objects.filter(user=request.user).order_by('-order_time'):
            items.append({'id': o.id, 'product': o.product_name, 'price': float(o.price), 'status': o.status, 'date': o.order_time})
        return JsonResponse({'orders': items})
    if request.method == 'POST':
        # create a simple order from posted product_id and quantity
        pid = request.POST.get('product_id')
        qty = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=pid)
        o = Order.objects.create(
            user=request.user,
            product_name=product.name,
            price=product.price,
            status='pending',
            order_time=date.today(),
        )
        return JsonResponse({'created': o.id}, status=201)
