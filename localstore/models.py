from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
import uuid

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)


class Seller(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    shop_name = models.CharField(max_length=255)
    shop_description = models.TextField(null=True, blank=True)
    entrepreneur_description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, upload_to='images/', default='images/default.jpg')
    mobile = models.CharField(max_length=10)
    contact = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          primary_key=True, editable=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_image = models.ImageField(
        null=True, blank=True, upload_to='images/', default='images/default.jpg')
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title.title()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def get_feedback_count(self):
        feedbacks = self.productfeedback_set.all()
        return feedbacks.count()

    @property
    def get_total_revenue(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.sub_total for item in orderitems])
        return total


class ProductImage(models.Model):
    uploaded = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True, upload_to='product-images/', default='images/no-image.png')


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          primary_key=True, editable=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          primary_key=True, editable=False)

    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.sub_total for item in orderitems])
        return total

    @property
    def get_order_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    id = models.UUIDField(unique=True, default=uuid.uuid4,
                          primary_key=True, editable=False)

    @property
    def sub_total(self):
        return self.product.unit_price * self.quantity

    @property
    def get_seller(self):
        return self.product.seller.id


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)

    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.sub_total for item in cartitems])
        return total

    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    id = models.UUIDField(unique=True, default=uuid.uuid4,

                          primary_key=True, editable=False)

    @property
    def sub_total(self):
        return self.product.unit_price * self.quantity


class ProductFeedback(models.Model):
    RATING_CHOICE = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    rating = models.CharField(max_length=1, choices=RATING_CHOICE, default='1')
    review = models.TextField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_seller(self):
        return self.product.seller.id


class Address(models.Model):
    PROVINCE = [
        ('1', 'Province 1'),
        ('2', 'Madhesh'),
        ('3', 'Bagmati'),
        ('4', 'Gandaki'),
        ('5', 'Lumbini'),
        ('6', 'Karnali'),
        ('7', 'Sudhur Pashchim'),
    ]
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, null=True)
    province = models.CharField(max_length=255, choices=PROVINCE)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)


class Vacancy(models.Model):
    TYPE = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time')
    ]
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    number_of_positions = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE, default='FT')
    min_salary = models.PositiveBigIntegerField()
    max_salary = models.PositiveBigIntegerField()
    location = models.CharField(max_length=255)
    posted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.title()
