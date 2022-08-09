from django import template
from localstore.models import Order
register = template.Library()


@register.filter(name='is_in_group')
def getUserGroup(user, group):
    return user.groups.filter(name=group).exists()


@register.filter(name='is_in_cart')
def getCartItem(user, product):
    customer = user.customer
    return customer.cart.cartitem_set.filter(product=product).exists()


@register.filter(name='has_ordered')
def getOrderItem(user, product):
    customer = user.customer
    orders = Order.objects.select_related('customer').all()
    for order in orders:
        if order.orderitem_set.filter(product=product).exists():
            print(True)
            return True


@register.filter(name='has_reviewed')
def getUserFeedback(user, product):
    customer = user.customer
    if customer.productfeedback_set.filter(product=product).exists():
        print(True)
    return customer.productfeedback_set.filter(product=product).exists()
