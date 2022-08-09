from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Seller, Product, Collection, ProductImage, Vacancy, ProductFeedback, Address, Customer


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input--style-4'})


class PortfolioForm(ModelForm):
    class Meta:
        model = Seller
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        
        self.fields['shop_name'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Shop Name"

        })
       
        self.fields['contact'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Contact"

        })
        self.fields['mobile'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Mobile Number"

        })
        self.fields['location'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Address"

        })
        self.fields['shop_description'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Tell something about your shop.."
        })
        self.fields['entrepreneur_description'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Tell something about yourself.."
        })


class JobForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'number_of_positions', 'type',
                  'min_salary', 'max_salary', 'location']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProductForm(ModelForm):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.all(), empty_label='Select a collection')

    class Meta:
        model = Product
        fields = ['title', 'description',
                  'inventory', 'unit_price', 'collection']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Product Name"

        })
        self.fields['description'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Product Description"

        })
        self.fields['inventory'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Number of items"

        })
        self.fields['unit_price'].widget.attrs.update({
            'class': "form-control",
            'placeholder': "Price of each product"

        })
        self.fields['collection'].widget.attrs.update({
            'class': "form-control",
        })


class ProductImageForm(ModelForm):

    class Meta:
        model = ProductImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'required': False,
            'name': 'image',
            'multiple': True,
        })


class ProductFeedbackForm(ModelForm):

    class Meta:
        model = ProductFeedback
        fields = ['rating', 'review']

    def __init__(self, *args, **kwargs):
        super(ProductFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({
            'class': 'form-control',


        })
        self.fields['review'].widget.attrs.update({
            'type': 'TextField',
            'class': 'form-control',

            'style': "resize: none"
        })


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['province', 'phone', 'city', 'address_1', 'address_2']
