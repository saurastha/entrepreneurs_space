from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from .forms import CustomUserCreationForm, PortfolioForm, ProductForm, JobForm, ProductImageForm, ProductFeedbackForm, AddressForm
from .models import User, Seller, Collection, Customer, Product, ProductImage, ProductFeedback, Cart, CartItem, Address, Order, OrderItem, Vacancy
import random

# Create your views here.

COLLECTION = Collection.objects.all()


def home(request):
    user = request.user

    if user.is_authenticated and user.groups.filter(name="Seller").exists():
        return redirect('seller-dashboard')

    queryset = Seller.objects.all()[:6]

    context = {'shops': list(queryset), 'collections': list(COLLECTION)}

    return render(request, 'localstore/index.html', context)


# View to Login All Users
def loginUsers(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exists!')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_seller:
                return redirect('seller-dashboard')
            elif 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('customer-main')

        else:
            messages.error(request, 'Username Or Password is incorrect.')
            return redirect('login')

    context = {'page': 'login'}
    return render(request, 'login.html', context)


# View to Register Seller
def registerSeller(request):
    form = CustomUserCreationForm()
    page = 'register'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_seller = True
            user.save()

            seller = Seller.objects.create(
                user=user,
            )
            messages.success(request, 'Account created succesfully!')

            login(request, user)
            return redirect('seller-dashboard')

    context = {'form': form, 'page': page}
    return render(request, 'register.html', context)


# View to Register Customer
def registerCustomer(request):
    form = CustomUserCreationForm()
    page = 'register'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()

            customer = Customer.objects.create(
                user=user
            )

            cart = Cart()
            cart.customer = customer
            cart.save()
            print(cart)

            login(request, user)
            return redirect('home')

    context = {'form': form, 'page': page}
    return render(request, 'register.html', context)


# View to Logout All Users
def logoutUsers(request):
    logout(request)
    return redirect('home')


def checkSeller(user):
    if user:
        return user.is_seller
    return False


def getSellerObjects(seller, queryset):
    related_queryset = []
    object_count = 0
    for object in queryset:
        get_seller = object.get_seller
        if get_seller == seller.id:
            related_queryset.append(object)
            object_count += 1

    return related_queryset, object_count


def getProductDetails(queryset):
    feedback_count = 0
    total_revenue = 0
    for object in queryset:
        feedback_count += object.get_feedback_count
        total_revenue += object.get_total_revenue

    return feedback_count, total_revenue


# View to Update Seller Portfolio


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def sellerDashboard(request):
    seller = request.user.seller
    product_queryset = seller.product_set.all().order_by('-last_updated')
    order_queryset = OrderItem.objects.select_related(
        'product__seller').all().order_by('-order__placed_at')

    orders, order_count = getSellerObjects(seller, order_queryset)

    feedback_count, total_revenue = getProductDetails(product_queryset)

    context = {'seller': seller,
               'recent_products': list(product_queryset[:5]),
               'recent_orders': list(orders[:5]),
               'order_count': order_count,
               'feedback_count': feedback_count,
               'total_revenue': total_revenue}
    return render(request, 'localstore/seller-template/dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def sellerProfile(request):
    seller = request.user.seller
    form = PortfolioForm(instance=seller)

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()

    context = {'form': form, 'seller': seller}
    return render(request, 'localstore/seller-template/seller-profile-form.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def sellerProduct(request):
    seller = request.user.seller
    queryset = seller.product_set.prefetch_related(
        'productimage_set').all()
    context = {'products': list(queryset), 'seller': seller}
    return render(request, 'localstore/seller-template/seller-products.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def addProduct(request):
    seller = request.user.seller
    image_form = ProductImageForm()
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)

        image_form = ProductImageForm(
            request.POST, request.FILES)

        files = request.FILES.getlist('image')

        if form.is_valid() and image_form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()

            for image in files:
                image = ProductImage.objects.create(
                    product=product, image=image)

            return redirect('seller-products')
    context = {'form': form, 'image_form': image_form, 'seller': seller}
    return render(request, 'localstore/seller-template/product-form.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def editProduct(request, pk):
    seller = request.user.seller
    product = seller.product_set.prefetch_related(
        'productimage_set').get(pk=pk)
    form = ProductForm(instance=product)
    image_form = ProductImageForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        image_form = ProductImageForm(
            request.POST, request.FILES)

        files = request.FILES.getlist('image')

        if form.is_valid() and image_form.is_valid():
            form.save()

            for image in files:
                image = ProductImage.objects.create(
                    product=product, image=image)
            return redirect('seller-products')

    context = {'form': form, 'image_form': image_form, 'product': product,
               'seller': seller, 'edit': True}
    return render(request, 'localstore/seller-template/product-form.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def viewProductFeedback(request):
    seller = request.user.seller

    feedback_queryset = ProductFeedback.objects.select_related('product').all()

    feedbacks,  count = getSellerObjects(seller, feedback_queryset)

    context = {'seller': seller, 'feedbacks': list(feedbacks)}
    return render(request, 'localstore/seller-template/product-feedback.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def viewOrderSeller(request):
    seller = request.user.seller
    order_queryset = OrderItem.objects.select_related(
        'product__seller').all()

    orders, order_count = getSellerObjects(seller, order_queryset)

    context = {'orderitems': list(orders), 'seller': seller}

    return render(request, 'localstore/seller-template/view-order-seller.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def deleteProduct(request, pk):
    seller = request.user.seller
    product = seller.product_set.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('seller-products')

    context = {'object': product, 'seller': seller}
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def deleteProductImage(request, pk):
    product_img = ProductImage.objects.get(pk=pk)
    product_img.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def postJob(request):
    seller = request.user.seller

    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.seller = seller
            job.save()

            return redirect('job-posted')

    context = {'seller': seller, 'form': form}
    return render(request, 'localstore/seller-template/post-job.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def editJob(request, pk):
    seller = request.user.seller
    job = seller.vacancy_set.get(pk=pk)
    form = JobForm(instance=job)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job-posted')
    context = {
        'seller': seller,
        'form': form
    }
    return render(request, 'localstore/post-job.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def deleteJob(request, pk):
    seller = request.user.seller
    job = seller.vacancy_set.get(pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job-posted')

    context = {'object': job, 'seller': seller}
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
@user_passes_test(checkSeller, login_url='access-denied')
def jobPosted(request):
    seller = request.user.seller
    jobs = seller.vacancy_set.all()
    context = {'seller': seller, 'jobs': jobs}
    return render(request, 'localstore/seller-template/job-posted.html', context)


# Customer Views
# Customer Views
def customerMain(request):
    seller_queryset = Seller.objects.all()[:6]
    product_queryset = Product.objects.prefetch_related(
        'productimage_set').all()[:6]
    # if seller_queryset.count() < 6:
    #     shops = seller_queryset
    # else:
    #     shops = random.sample(seller_queryset, 6)
    # if product_queryset.count() < 6:
    #     products = product_queryset
    # else:
    #     products = random.sample(product_queryset, 6)

    context = {'shops': list(seller_queryset), 'products': list(product_queryset),
               'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/customer.html', context)


def allShop(request):
    shops = Seller.objects.all()
    context = {'collections': list(COLLECTION), 'shops': list(shops)}
    return render(request, 'localstore/customer-template/all-shop.html', context)


def allCollection(request):
    context = {'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/all-collection.html', context)


def shop(request, pk):
    shop = Seller.objects.prefetch_related('product_set').get(pk=pk)

    products = Product.objects.filter(seller=shop)
    context = {'collections': list(
        COLLECTION), 'shop': shop, 'products': products}
    return render(request, 'localstore/customer-template/browse-shop.html', context)


def collectionProduct(request, pk):
    collection = Collection.objects.get(pk=pk)
    products = Product.objects.filter(collection=collection)
    context = {'collection': collection,
               'products': products, 'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/collection-product.html', context)


def allProduct(request):
    products = Product.objects.prefetch_related(
        'productimage_set').all()

    context = {'products': products, 'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/all-product.html', context)


def viewProduct(request, pk):
    print(request.user)
    product = Product.objects.prefetch_related(
        'productimage_set').prefetch_related('productfeedback_set').get(pk=pk)
    print(product.inventory)
    form = ProductFeedbackForm()

    if request.method == 'POST':
        form = ProductFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.product = product
            feedback.customer = request.user.customer
            feedback.save()

        return redirect(request.META.get('HTTP_REFERER'))

    context = {'product': product, 'form': form,
               'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/view-product.html', context)


@login_required(login_url='login')
def addCart(request, product_pk):
    customer = request.user.customer
    product = Product.objects.get(pk=product_pk)

    cart = customer.cart

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except:
        cart_item = CartItem()
        cart_item.cart = cart
        cart_item.product = product
        cart_item.quantity = 1
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def removeCart(request, product_pk):
    customer = request.user.customer
    product = Product.objects.get(pk=product_pk)
    cart = Cart.objects.get(customer=customer)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required(login_url='login')
def removeCartItem(request, product_pk):
    customer = request.user.customer
    product = Product.objects.get(pk=product_pk)
    cart = customer.cart
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()

    return redirect('cart')


@login_required(login_url='login')
def cart(request, total=0, quantity=0, cart_items=None):

    customer = request.user.customer
    try:
        cart = customer.cart
        print(cart)
        cart_items = CartItem.objects.select_related(
            'product').filter(cart=cart)
        print(cart_items)
        total = cart.get_cart_total
        quantity = cart.get_cart_items
    except ObjectDoesNotExist:
        pass

        return redirect('home')

    context = {
        'total': total, 'collections': list(COLLECTION),
        'quantity': quantity,
        'cart_items': list(cart_items)
    }

    return render(request, 'localstore/customer-template/product-cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, cart_items=None):
    customer = request.user.customer

    cart = customer.cart
    cart_items = CartItem.objects.select_related(
        'product').filter(cart=cart)
    if cart_items.count() == 0:
        return redirect('cart')

    try:
        address = customer.address
    except ObjectDoesNotExist:
        address = Address()
        address.customer = customer
        address.save()
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    context = {'form': form, 'customer': customer,
               'cart': cart, 'cart_items': list(cart_items), 'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/checkout.html', context)


@login_required(login_url='login')
def createOrder(request):
    customer = request.user.customer
    cart = customer.cart
    cart_items = CartItem.objects.select_related(
        'product').filter(cart=cart)
    if cart_items.count() == 0:
        return redirect('view-order')
    with transaction.atomic():
        order = Order()
        order.customer = customer
        order.save()
        for item in cart_items:
            orderitem = OrderItem()
            orderitem.order = order
            orderitem.product = item.product
            orderitem.quantity = item.quantity
            orderitem.unit_price = item.product.unit_price
            product = Product.objects.get(pk=orderitem.product.id)
            product.inventory -= orderitem.quantity
            product.save()

            orderitem.save()
            item.delete()

    orderitems = order.orderitem_set.all()

    context = {'order': order,
               'orderitems': orderitems, 'customer': customer, 'collections': list(COLLECTION)}

    return render(request, 'localstore/customer-template/invoice.html', context)


@login_required(login_url='login')
def viewInvoice(request, pk):
    customer = request.user.customer
    order = customer.order_set.prefetch_related(
        'orderitem_set').get(pk=pk)
    orderitems = order.orderitem_set.all()

    context = {'order': order, 'orderitems': orderitems,
               'customer': customer, 'collections': list(COLLECTION), 'page': 'invoice'}
    return render(request, 'localstore/customer-template/invoice.html', context)


@login_required(login_url='login')
def viewOrderCustomer(request):
    customer = request.user.customer
    orders = customer.order_set.prefetch_related(
        'orderitem_set').all().distinct().order_by('-placed_at')

    context = {'orders': list(orders), 'collections': list(COLLECTION)}
    return render(request, 'localstore/customer-template/view-order-customer.html', context)


def vacancy(request):
    vacancies = Vacancy.objects.all()

    context = {'collections': list(COLLECTION), 'vacancies': list(vacancies)}
    return render(request, 'localstore/customer-template/vacancy.html', context)


def searchResult(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    products = Product.objects.filter(title__icontains=search_query)
    shops = Seller.objects.filter(Q(shop_name__icontains=search_query) | Q(
        description__icontains=search_query))

    context = {'products': products, 'shops': shops,
               'search_query': search_query, 'collections': list(COLLECTION)}
    return render(request, 'localstore/search-result.html', context)


def forbidden(request):
    return render(request, 'forbidden.html')


def termsAndConditions(request):
    return render(request, 'terms-and-conditions.html')


def faq(request):
    return render(request, 'faq.html')
