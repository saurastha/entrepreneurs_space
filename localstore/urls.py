from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register-seller/', views.registerSeller, name='register-seller'),
    path('seller-dashboard/', views.sellerDashboard, name='seller-dashboard'),
    path('seller-profile/', views.sellerProfile, name='seller-profile'),
    path('seller-products/', views.sellerProduct, name='seller-products'),
    path('add-product/', views.addProduct, name='add-product'),
    path('edit-product/<str:pk>', views.editProduct, name='edit-product'),
    path('product-feedback/', views.viewProductFeedback, name='product-feedback'),
    path('view-order-seller/', views.viewOrderSeller, name='view-order-seller'),
    path('delete-product/<str:pk>/', views.deleteProduct, name='delete-product'),
    path('delete-product-img/<str:pk>/',
         views.deleteProductImage, name='delete-product-img'),
    path('post-job/', views.postJob, name='post-job'),
    path('edit-job/<str:pk>', views.editJob, name='edit-job'),
    path('job-posted/', views.jobPosted, name='job-posted'),
    path('delete-job/<str:pk>/', views.deleteJob, name='delete-job'),


    path('search-result/', views.searchResult, name='search-result'),

    path('shops/', views.allShop, name='shops'),
    path('shop/<str:pk>', views.shop, name='shop'),
    path('collections/', views.allCollection, name='collections'),
    path('collection/<str:pk>', views.collectionProduct, name='collection-product'),

    path('customer-main/', views.customerMain, name='customer-main'),
    path('register-customer/', views.registerCustomer, name='register-customer'),
    path('all-products/', views.allProduct, name='all-product'),
    path('product/<str:pk>/', views.viewProduct, name='view-product'),
    path('add-cart/<str:product_pk>/', views.addCart, name='add-cart'),
    path('remove-cart/<str:product_pk>/', views.removeCart, name='remove-cart'),
    path('remove-cart-item/<str:product_pk>/',
         views.removeCartItem, name='remove-cart-item'),
    path('cart/', views.cart, name='cart'),
    path('checko`ut/', views.checkout, name='checkout'),
    path('create-order/', views.createOrder, name='create-order'),
    path('view-order/', views.viewOrderCustomer, name='view-order'),
    path('invoice/<str:pk>', views.viewInvoice, name='invoice'),
    path('vacancy/', views.vacancy, name='vacancy'),


    path('login/', views.loginUsers, name='login'),
    path('logout/', views.logoutUsers, name='logout'),
    path('access-denied/', views.forbidden, name='access-denied'),
    path('FAQs/', views.faq, name='faq'),
    path('terms-and-conditions/', views.termsAndConditions,
         name='terms-and-conditions'),
]
