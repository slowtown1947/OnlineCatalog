from django.forms import ModelForm
from .models import PhoneModel, PhoneCategoryModel
from django import forms

class PhoneModelForm(ModelForm):
    class Meta:
        model = PhoneModel
        fields = ['phone_name', 'phone_description', 'phone_image', 'phone_price']

class OrderForm(forms.Form):
    address = forms.CharField(label='Delivery Address', max_length=100)
    phone = forms.CharField(label='Phone', max_length=15)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', max_length=100)

class UserProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    # phone_number = forms.CharField(label='Phone Number', max_length=15)
    # address = forms.CharField(label='Address', widget=forms.Textarea)

class PhoneCategoryForm(forms.Form):
    categories = PhoneCategoryModel.objects.all()
    category_choices = []
    for cat in categories:
        category_choices.append((cat.cat_url, cat.cat_name))

    category = forms.ChoiceField(choices=category_choices)
