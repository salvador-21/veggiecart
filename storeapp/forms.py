from django import forms
import django.forms.utils
import django.forms.widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserAccount,UserWallet,UserProfile,Product,ProductPrice,ProductImage,Address
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator

USERTYPE=(
    ('','-------'),
    ('CUSTOMER','CUSTOMER'),
    ('FARMER','FARMER'),
    ('ADMIN','ADMIN'),
)

class LoginForm(forms.Form):
    
    username=forms.CharField(label="Username",max_length=50, widget=forms.TextInput(attrs={'autocomplete':'off','placeholder':'Username','class':'form-control bg-white border-0 ps-0'}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control bg-white border-0 ps-0'}))
   

class SignUpForm(forms.ModelForm):
    first_name=forms.CharField(label='First Name',max_length=50, widget=forms.TextInput(attrs={'placeholder':'Firstname','class':'form-control bg-white border-0 ps-0'}))
    last_name=forms.CharField(label='Last Name',max_length=50, widget=forms.TextInput(attrs={'placeholder':'LastName','class':'form-control bg-white border-0 ps-0'}))
    email=forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'minlength':'10','placeholder':'Email Address','class':'form-control bg-white border-0 ps-0'}))
    contact_no=forms.CharField(label='Contact',max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter mobile number', 'type': 'tel','class':'form-control bg-white border-0 ps-0'}))
    username=forms.CharField(label='Username',max_length=50, widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control bg-white border-0 ps-0'}))
    password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control bg-white border-0 ps-0 pass1'}))
    confirm_password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder':' Confirm Password','class':'form-control bg-white border-0 ps-0 pass2'}))
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','email','contact_no','username', 'password')

class UserForm(ModelForm):
    contact_no=forms.IntegerField(label='Contact', widget=forms.NumberInput(attrs={'minlength':'10','placeholder':'Mobile Number','class':'form-control inputclass'}))
    usertype=forms.ChoiceField(label='Account Type',widget=forms.Select(attrs={'class':'form-control inputclass bg-dark'}), choices=USERTYPE)
    class Meta:
        model = UserAccount
        fields=('usertype',)

WALLET_STATUS=(
    ('ACTIVE','ACTIVE'),
    ('ONHOLD','ONHOLD'),
    ('BANNED','BANNED'),
)
PRODUCT_CATEGORY=(
    ('VEGETABLE','VEGETABLE'),
    ('FRUIT','FRUIT'),
    ('CROP','CROP'),
)
PRODUCT_UNIT=(
    ('Kilograms (kg)','Kilograms (kg)'),
    ('Pieces (pcs)','Pieces (pcs)'),
)
class WalletForm(ModelForm):
    w_balance=forms.IntegerField(label='Balance', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control inputclass'}))
    w_points=forms.IntegerField(label='Points', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control inputclass'}))
    w_commission=forms.IntegerField(label='Commission', widget=forms.NumberInput(attrs={'maxlength':'2','placeholder':'0','class':'form-control inputclass'}))
    w_status=forms.ChoiceField(label='Status',widget=forms.Select(attrs={'class':'form-control inputclass'}), choices=PRODUCT_CATEGORY)
    class Meta:
        model = UserWallet
        fields=('w_balance','w_points','w_commission',)


class ProductForm(ModelForm):
    prod_name=forms.CharField(label='Product Name',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Product Name','class':'form-control inputclass'}))
    prod_desc=forms.CharField(label='Product Description',max_length=100, widget=forms.TextInput(attrs={'placeholder':'Product Description','class':'form-control inputclass'}))
    prod_category=forms.ChoiceField(label='Product Category',widget=forms.Select(attrs={'class':'form-control inputclass'}), choices=PRODUCT_CATEGORY)
    class Meta:
        model = Product
        fields=('prod_name','prod_desc','prod_category')

class ProductPriceForm(ModelForm):
    p_qty=forms.IntegerField(label='Product Quantity', widget=forms.NumberInput(attrs={'maxlength':'5','placeholder':'0','class':'form-control inputclass'}))
    p_unit=forms.ChoiceField(label='Product Unit',widget=forms.Select(attrs={'class':'form-control inputclass'}), choices=PRODUCT_UNIT)
    p_price=forms.IntegerField(label='Product Price', widget=forms.NumberInput(attrs={'maxlength':'5','placeholder':'0','class':'form-control inputclass'}))
    class Meta:
        model = ProductPrice
        fields=('p_qty','p_unit','p_price')

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields=('pi_image',)
    pi_image=forms.FileField(label='Product Image', widget=forms.FileInput(attrs={'class':'form-control inputclass',}))

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields='__all__'
