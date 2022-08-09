from urllib import request
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal, receiver
from .models import Customer, Cart
# create_user = Signal('request')


# @receiver(create_user)
# def customCreateUser(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         print(user.groups.filter(name='Seller').exists())
#         if user.groups.filter(name='Seller').exists():
#             seller = Seller.objects.create(
#                 user=user,
#                 username=user.username,
#                 email=user.email,
#                 name=f'{user.first_name} {user.last_name}',
#             )

#     Signal.disconnect()


# def createCart(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         print(user.groups.filter(name='Customer').exists())
#         if user.groups.filter(name='Customer').exists():
#             cart = Cart.objects.create(
#                 customer=user.customer
#             )


# post_save.connect(createCart, sender=User)
