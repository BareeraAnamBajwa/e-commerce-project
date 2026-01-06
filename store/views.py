from datetime import datetime
from django.shortcuts import redirect, render , get_object_or_404
from django.db import OperationalError
from .models import Product, cart , Address, Slider, Promotion, Brand, SiteSettings, FooterLink, Review, Category, SubCategory
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.shortcuts import render



def index(request):
    return render(request, 'store/index.html')  # your home page template

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def index_view(request):
    trending_items = Product.objects.all()[:6]
    mobile_phones = Product.objects.filter(category__category_id__name="Mobile")
    tablets = Product.objects.filter(category__category_id__name="Tablet")
    user_carts = cart.objects.filter(user_id=request.user)
    
    # Dynamic content - handle case when tables don't exist yet
    try:
        sliders = Slider.objects.filter(is_active=True)
    except OperationalError:
        sliders = []
    
    try:
        promotions = Promotion.objects.filter(is_active=True)
    except OperationalError:
        promotions = []
    
    try:
        brands = Brand.objects.filter(is_active=True)
    except OperationalError:
        brands = []
    
    return render(request, "store/index.html", {
        "trending_items": trending_items,
        "mobile_phones": mobile_phones,
        "tablets": tablets,
        "carts": user_carts,
        "sliders": sliders,
        "promotions": promotions,
        "brands": brands,
    })

@login_required

def checkout_cart_view(request):
    user_carts = cart.objects.filter(user_id=request.user)
    cart_quantity = sum(cart_item.quantity * cart_item.total for cart_item in user_carts)
    cart_subtotal = sum(cart_item.grand_total for cart_item in user_carts)
    return render(request, 'store/checkout_cart.html',{'carts':user_carts , 'cart_subtotal':cart_subtotal , "cart_quantity":cart_quantity})


def checkout_complete_view(request):
    user_carts = cart.objects.filter(user_id=request.user) if request.user.is_authenticated else []
    cart_quantity = sum(cart_item.quantity * cart_item.total for cart_item in user_carts)
    cart_subtotal = sum(cart_item.grand_total for cart_item in user_carts)
    return render(request, "store/checkout_complete.html" , {'carts':user_carts , 'cart_subtotal':cart_subtotal , "cart_quantity":cart_quantity})

@login_required
def checkout_info_view(request):
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('first_name') or None
        last_name = request.POST.get('last_name') or None
        address = request.POST['address']
        area_code = int(request.POST['area_code'])
        phone_number = int(request.POST['phone_number'])
        zip_code = int(request.POST['zip_code'])
        company = request.POST.get('company') or None
        business = 'business' in request.POST  # Check if checkbox was checked

        # Create and save new Address instance with user
        Address.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            area_code=area_code,
            phone_number=phone_number,
            zip_code=zip_code,
            company=company,
            business=business
        )
        
        # Store total amount in session for payment
        user_carts = cart.objects.filter(user_id=request.user)
        total_amount = sum(cart_item.grand_total for cart_item in user_carts)
        request.session['total_amount'] = float(total_amount)
        
        return redirect("checkout_payment")
    return render(request, "store/checkout_info.html")
        


def contact_us_view(request):
    return render(request, "store/contact_us.html")


def faq_view(request):
    return render(request, "store/faq.html")


def index_fixed_view(request):
    return render(request, "store/index_fixed_header.html")


def index_inverse_header_view(request):
    return render(request, "store/index_inverse_header.html")


def my_account_view(request):
    return render(request, "store/my_account.html")

@login_required
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_carts = cart.objects.filter(user_id=request.user)
    all_products = Product.objects.exclude(id=product_id)[:6]
    
    try:
        product_images = product.images.all()
    except OperationalError:
        product_images = []
    
    try:
        reviews = Review.objects.filter(product=product, is_approved=True)
    except OperationalError:
        reviews = []
    
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = cart.objects.get_or_create(
            user_id=request.user,
            pro_id=product,
            )
        
        if not created:
            cart_item.quantity += 1
            
        cart_item.total = product.price
        cart_item.grand_total = cart_item.total * cart_item.quantity
        cart_item.save()
        return redirect('product_detail', product_id=product_id)
            
    return render(request, "store/product_detail.html" , {
        "product": product,
        "all_products": all_products,
        "carts": user_carts,
        "product_images": product_images,
        "reviews": reviews,
    })


def product_view(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    
    try:
        brands = Brand.objects.filter(is_active=True)
    except OperationalError:
        brands = []
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        all_products = all_products.filter(category__category_id__name=category_filter)
    
    # Filter by brand if provided
    brand_filter = request.GET.get('brand')
    if brand_filter:
        all_products = all_products.filter(name__icontains=brand_filter)
    
    return render(request, "store/product.html" , {
        "all_products": all_products,
        "categories": categories,
        "brands": brands,
    })


def search_results_view(request):
    query = request.GET.get('q', '')
    all_products = Product.objects.all()
    
    if query:
        all_products = Product.objects.filter(
            name__icontains=query
        ) | Product.objects.filter(
            features__icontains=query
        )
    
    # Filter by price range
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    if price_from:
        all_products = all_products.filter(price__gte=float(price_from))
    if price_to:
        all_products = all_products.filter(price__lte=float(price_to))
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        all_products = all_products.filter(category__category_id__name=category_filter)
    
    categories = Category.objects.all()
    
    return render(request, "store/search_results.html", {
        "all_products": all_products,
        "query": query,
        "categories": categories,
    })


def about_us_view(request):
    return render(request, "store/about_us.html")


@login_required
def checkout_payment_view(request):
    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number').replace(' ', '')
        exp_month = request.POST.get('exp_month')
        exp_year = request.POST.get('exp_year')
        csc = request.POST.get('csc')

        total_amount = request.session.get('total_amount', 0) 
        if total_amount <= 0:
            return render(request, "store/checkout_payment.html", {'error': 'Invalid payment amount'})

        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'cardholder_name':cardholder_name,
                    'number': card_number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': csc,
                },
            )

            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),
                currency='usd',
                payment_method=payment_method.id,
                confirm=True,
            )

            if payment_intent.status == 'succeeded':
                # Clear cart after successful payment
                cart.objects.filter(user_id=request.user).delete()
                return redirect('checkout_complete')
            else:
                return render(request, "store/checkout_payment.html", {'error': 'Payment failed'})

        except stripe.error.StripeError as e:
            return render(request, "store/checkout_payment.html", {'error': str(e)})
        except Exception as e:
            return render(request, "store/checkout_payment.html", {'error': 'An error occurred'})

    return render(request, "store/checkout_payment.html", {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def update_cart_quantity(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(cart, id=cart_id, user_id=request.user)
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        cart_item.grand_total = cart_item.total * cart_item.quantity
        cart_item.save()
    
    return redirect('checkout_cart')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(cart, id=cart_id, user_id=request.user)
    cart_item.delete()
    return redirect('checkout_cart')

@login_required
def submit_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        message = request.POST.get('review', '')
        
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            title=title,
            message=message
        )
    
    return redirect('product_detail', product_id=product_id)

@login_required
def add_product_view(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        warranty = request.POST.get('warranty')
        availability = request.POST.get('availability')
        price = request.POST.get('price')
        original_price = request.POST.get('original_price') or None
        discount = request.POST.get('discount') or None
        features = request.POST.get('features')
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url') or None
        
        # Validate required fields
        if name and category_id and warranty and availability and price and features:
            try:
                category = SubCategory.objects.get(id=category_id)
                product = Product.objects.create(
                    name=name,
                    category=category,
                    warranty=warranty,
                    availability=availability,
                    price=float(price),
                    original_price=float(original_price) if original_price else None,
                    discount=int(discount) if discount else None,
                    features=features,
                    image=image,
                    image_url=image_url
                )
                return redirect('product_detail', product_id=product.id)
            except Exception as e:
                error_message = f"Error creating product: {str(e)}"
                subcategories = SubCategory.objects.all()
                return render(request, 'store/add_product.html', {
                    'subcategories': subcategories,
                    'error': error_message
                })
        else:
            error_message = "Please fill all required fields"
            subcategories = SubCategory.objects.all()
            return render(request, 'store/add_product.html', {
                'subcategories': subcategories,
                'error': error_message
            })
    
    # GET request - show form
    subcategories = SubCategory.objects.all()
    return render(request, 'store/add_product.html', {
        'subcategories': subcategories
    })