from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product


# ----------------------------
# Product list page
# ----------------------------
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})


# ----------------------------
# Product detail page
# ----------------------------
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


# ----------------------------
# Add to cart
# ----------------------------
def add_to_cart(request, id):
    cart = request.session.get('cart', [])
    cart.append(id)
    request.session['cart'] = cart
    return redirect('cart')


# ----------------------------
# Cart page
# ----------------------------
def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })


# ----------------------------
# Place order
# ----------------------------
def place_order(request):
    request.session['cart'] = []
    return render(request, 'store/order_success.html')


# ============================
# AUTHENTICATION
# ============================

# ----------------------------
# Signup page
# ----------------------------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'store/signup.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )
        login(request, user)
        return redirect('products')

    return render(request, 'store/signup.html')


# ----------------------------
# Login page
# ----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('products')
        else:
            return render(request, 'store/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'store/login.html')


# ----------------------------
# Logout
# ----------------------------
def logout_view(request):
    logout(request)
    return redirect('login')