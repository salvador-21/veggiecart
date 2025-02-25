from django.utils.timezone import localtime
from django.db import models
from django.db.models.deletion import RESTRICT,CASCADE
from django.contrib.auth.models import User,AbstractUser
import uuid
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

now=timezone.now

class UserProfile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_joined=models.DateTimeField(default=now)
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField(unique=True)

    def get_local_start_time(self):
        return localtime(self.date_joined)
    
class UserAccount(models.Model):
    user=models.OneToOneField(UserProfile,on_delete=CASCADE,related_name='useraccount')
    contact_no=models.CharField(unique=True,max_length=12, blank=False, null=False,default='+63000000000')
    referral_code=models.CharField(max_length=50,null=True, blank=True)
    usertype=models.CharField(max_length=50,default='ADMIN', choices=[('CLIENT','CLIENT'),('FARMER','FARMER'),('ADMIN','ADMIN'),('SUPER ADMIN','SUPER ADMIN')]) 
    status=models.CharField(max_length=50,default='NOT VERIFIED',choices=[('NOT VERIFIED','NOT VERIFIED'),('VERIFIED','VERIFIED')])
    def __str__(self):
        return str(self.user.username+' - '+self.usertype)
        
    def __str__(self):
        return str(self.user.username)

class Address(models.Model):
    user=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='address')
    ad_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    ad_name=models.CharField(max_length=200,null=True, blank=True)
    ad_region=models.CharField(max_length=50,null=True, blank=True)
    ad_state=models.CharField(max_length=50,null=True, blank=True)
    ad_lat=models.CharField(max_length=50,null=True, blank=True)
    ad_long=models.CharField(max_length=50,null=True, blank=True)
    ad_desc=models.CharField(max_length=100,null=True, blank=True)
    ad_type=models.CharField(max_length=50,default='HOME', choices=[('HOME','HOME'),('WORK','WORK'),('CUSTOM','CUSTOM')]) 
    ad_status=models.CharField(max_length=50,default='INACTIVE', choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE')]) 
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au
    def __str__(self):
        return str(str(self.user)+ '-'+str(self.ad_region)+'-' +self.ad_type)

class UserWallet(models.Model):
    user=models.OneToOneField(UserProfile, on_delete=CASCADE)
    w_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    w_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_points=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_commission=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    w_status=models.CharField(max_length=50,default='ACTIVE',choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE'),('BANNED','BANNED')])

    def __str__(self):
        return str(self.user.username +' - '+str(self.w_id))
    
class ProductImage(models.Model):
    pi_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    pi_image=models.ImageField(blank=True, null=True ,upload_to='uploads')

    def __str__(self):
        return str(self.pi_image )
    
class ProductPrice(models.Model):
    p_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    p_qty=models.IntegerField(null=True, blank=True, default=0)
    p_unit=models.CharField(max_length=50,default='Kilograms (kg)',choices=[('Kilograms (kg)','Kilograms (kg)'),('Pieces (pcs)','Pieces (pcs)')])
    p_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return str(self.p_qty)+' - '+str(self.p_unit)
    
class Product(models.Model):
    user=models.ForeignKey(UserProfile, default=uuid.uuid4,on_delete=CASCADE,related_name='product')
    prod_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    prod_name=models.CharField(max_length=50,null=True, blank=True)
    prod_desc=models.CharField(max_length=100,null=True, blank=True)
    prod_category=models.CharField(max_length=50,default='VEGETABLE',choices=[('VEGETABLE','VEGETABLE'),('FRUIT','FRUIT'),('CROP','CROP')])
    prod_status=models.CharField(max_length=50,default='UNAVAILABLE',choices=[('AVAILABLE','AVAILABLE'),('OUT OF STOCK','OUT OF STOCK'),('UNAVAILABLE','UNAVAILABLE')])
    image=models.ForeignKey(ProductImage,default=uuid.uuid4,on_delete=CASCADE,related_name='product')
    pricing=models.ForeignKey(ProductPrice,default=uuid.uuid4,on_delete=CASCADE,related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au
    def __str__(self):
        return str(self.prod_name)+'  - '+str(self.prod_status)


class Cart(models.Model):
    product=models.ForeignKey(Product,default=uuid.uuid4,on_delete=CASCADE,related_name='cart_poduct')
    user=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='cart_user')
    cart_product_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cart_code=models.CharField(max_length=50,null=True, blank=True)
    cart_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    cart_unit=models.CharField(max_length=50,null=True, blank=True)
    cart_qty=models.IntegerField(null=True, blank=True, default=0)
    cart_price=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cart_status=models.CharField(max_length=50,default='PENDING',choices=[('ORDERED','ORDERED'),('PENDING','PENDING'),('DONE','DONE')])
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au
    def __str__(self):
        return str(self.product )

class Order(models.Model):
    user=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='order_user')
    order_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    order_code=models.CharField(max_length=50,null=True, blank=True)
    order_payment=models.CharField(max_length=50,null=True, blank=True)
    order_status=models.CharField(max_length=50,default='PENDING',choices=[('PENDING','PENDING'),('TO PAY','TO PAY'),('TO SHIP','TO SHIP'),('TO RECEIVE','TO RECEIVE'),('COMPLETED','COMPLETED'),('CANCELLED','CANCELLED')])
    order_total=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_shipping=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au

    def __str__(self):
        return str(self.user)+' - '+str(self.order_code)
    
class OrderDetails(models.Model):
    user=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='od_user')
    od_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    od_code=models.CharField(max_length=50,null=True, blank=True)
    product=models.ForeignKey(Product,default=uuid.uuid4,on_delete=CASCADE,related_name='od_poduct')
    od_prodname=models.CharField(max_length=50,null=True, blank=True)
    od_qty=models.IntegerField(null=True, blank=True, default=0)
    od_unit=models.CharField(max_length=50,null=True, blank=True)
    od_price=models.IntegerField(null=True, blank=True, default=0)
    od_status=models.CharField(max_length=50,default='PENDING',choices=[('PENDING','PENDING'),('TO PAY','TO PAY'),('TO SHIP','TO SHIP'),('TO RECEIVE','TO RECEIVE'),('COMPLETED','COMPLETED'),('CANCELLED','CANCELLED')])
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au
    def __str__(self):
        return str(self.user)+' - '+str(self.od_code)
    

class Promo(models.Model):
    user=models.ForeignKey(UserProfile,default=uuid.uuid4,on_delete=CASCADE,related_name='promo_user')
    promo_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    min_cost=models.IntegerField(null=True, blank=True, default=0)
    promo_type=models.CharField(max_length=50,default='FREE DELIVERY',choices=[('FREE DELIVERY','FREE DELIVERY'),('VOUCHER','VOUCHER')])
    deduction=models.IntegerField(null=True, blank=True, default=0)
    promo_status=models.CharField(max_length=50,default='ACTIVE',choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE')])
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au



class TransferHistory(models.Model):
    from_user=models.CharField(max_length=50,null=True, blank=True)
    t_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    t_product=models.CharField(max_length=50,null=True, blank=True)
    t_desc=models.CharField(max_length=100,null=True, blank=True)
    t_qty=models.IntegerField(null=True, blank=True, default=0)
    to_user=models.CharField(max_length=50,null=True, blank=True)
    t_action=models.CharField(max_length=50,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Au
    def __str__(self):
        return str(self.from_user)
