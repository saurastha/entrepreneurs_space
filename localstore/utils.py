from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Seller, Customer


def registration(request, page_for):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if page_for == 'seller':
                group = Group.objects.get(name='Seller')
                group.user_set.add(user)
                seller = Seller.objects.create(
                    user=user,
                    username=user.username,
                    email=user.email,
                    name=f'{user.first_name} {user.last_name}',
                )
            elif page_for == 'customer':
                group = Group.objects.get(name='Customer')
                group.user_set.add(user)
                customer = Customer.objects.create(
                    user=user,
                    username=user.username,
                    email=user.email,
                    name=f'{user.first_name} {user.last_name}',
                )

                messages.success(request, 'Account created succesfully!')

                login(request, user)
                return True
        else:
            messages.error(request, 'Error')
