from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm,LoginForm,UserForm,WalletForm,ProductForm,ProductPriceForm,ProductImageForm,AddressForm
import uuid
from .models import Address,UserAccount,UserProfile,UserWallet,ProductPrice,Product,ProductImage,Cart,TransferHistory,Order,OrderDetails
from django.db.models import Q ,OuterRef, Subquery, F, Value
from django.db.models.functions import Concat
from django.db.models import TextField
import folium
from folium.plugins import FastMarkerCluster
import requests
import json
import random
import string

# Function to generate a random string of a given length
def order_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# Create your views here.


# @receiver(post_save, sender=UserProfile)
# def create_user_account(sender, instance, created, **kwargs):
#     if created:
#         UserAccount.objects.create(user=instance)

# @receiver(post_save, sender=UserProfile)
# def save_user_account(sender, instance, **kwargs):
#     instance.useraccount.save()

def index(request):
    if request.user.is_authenticated:
        
          return redirect('homepage')
    else:
        context={
            'page':'HOMEPAGE',
            'login_frm':LoginForm(),
            'signup_frm':SignUpForm()
        }
        return render(request,'storeapp/homepage/index.html',context)

def homepage(request):
    try:
        address=Address.objects.get(user=request.user, ad_status='ACTIVE')
    except Exception as e:
        address=''
    try:
        if(request.user.useraccount.usertype == 'ADMIN'):
            domain = request.get_host()
            reglink=domain+'/farmer/reg/'+str(request.user.id)
        else:
            reglink=''
    except Exception as e:
        reglink=''

    print(request.user.useraccount.usertype)
    
    context={
         'page':'HOMEPAGE',
         'product_frm':ProductForm(),
         'productPrice_frm':ProductPriceForm(),
         'productImage_frm':ProductImageForm(),
         'farmer_link':reglink,
         'address':address,

    }
    try:
        if(request.user.useraccount.usertype == 'ADMIN'):
            return render(request,'storeapp/admin/index2.html',context)  
        elif(request.user.useraccount.usertype == 'FARMER'):
            return render(request,'storeapp/farmer/index.html',context)
        elif(request.user.useraccount.usertype == 'CLIENT'):
            return render(request,'storeapp/client/index.html',context)
     
        
    except Exception as e:
        return render(request,'storeapp/homepage/404.html',context)

    
    
     



def auth_user(request):
     form = LoginForm(request.POST or None)
     msg=''
     if request.method == 'POST':
          if form.is_valid():
               username=form.cleaned_data.get('username')
               password=form.cleaned_data.get('password')
            #    user=authenticate(username=username.upper(), password=password)
               user=authenticate(username=username, password=password)
               print(user)
               if user is not None:
                    msg='login'
                    login(request,user)
                    status=1
               else:
                    status=0
                    msg='err'
          else:
              status=0
              msg='not valid'
     return JsonResponse({'data':msg})

def signup(request):

    if request.method == 'POST':
         
         acc= SignUpForm(data=request.POST)
         userinfo=UserForm()
         walletform=WalletForm()
         if acc.is_valid():
            user = acc.save()
            user.set_password(user.password)
            user.save()
            info = userinfo.save(commit = False)
            info.user = user
            info.contact_no=request.POST.get('contact_no')
            info.usertype=request.POST.get('usertype')
            info.status='ACTIVE'
            info.save()
            wall=walletform.save(commit = False)
            wall.user=user
            wall.w_balance=0
            wall.w_points=0
            wall.w_commission=0
            wall.w_status='ACTIVE'
            wall.save()

            username=acc.cleaned_data.get('username')
            password=acc.cleaned_data.get('password')
            login_user=authenticate(username=username, password=password)
            login(request,login_user)
            msg='valid'
            return JsonResponse({'data':msg})
         else:
              msg='invalid'
              print(acc.errors)
              return JsonResponse({'data':acc.errors})
    
    


def signout(request):
    logout(request)
    
    return redirect('/')

def profile(request):
     context={
          'page':'PROFILE',
          
     }
     return render(request,'storeapp/homepage/profile.html',context)

def cart(request,user):
    address=Address.objects.filter(user=request.user)
    
    context={
          'page':'CART',
          'my_add': list(address)
     }
    return render(request,'storeapp/homepage/cart.html',context)



def save_address(request):
     
     name=request.POST.get('ad_name')
     region=request.POST.get('ad_region')
     state=request.POST.get('ad_state')
     lat=request.POST.get('ad_lat')
     lng=request.POST.get('ad_lng')
     desc=request.POST.get('ad_desc')
     atype=request.POST.get('ad_type')
     s_address=Address.objects.create(user=request.user, ad_name=name,ad_region=region,ad_state=state,ad_lat=lat,ad_long=lng,ad_desc=desc,ad_type=atype).save()
     print(s_address)
     return JsonResponse({'data':s_address})

@csrf_exempt
def up_address(request):
    adid=request.POST.get('adid')
    g_up=Address.objects.filter(Q(user=request.user) & ~Q(ad_id=adid)).update(ad_status='INACTIVE') 
    g_cup=Address.objects.get(ad_id=adid)
    g_cup.ad_status='ACTIVE'
    g_cup.save()

    return JsonResponse({'data':'ok'})

def get_address(request):
    try:
        g_add = Address.objects.values('ad_id','ad_name','ad_type','ad_status').filter(user=request.user)
        ad = list(g_add)
        return JsonResponse(ad, safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

def add_product(request):
    
     frm_product=ProductForm(request.POST)
     frm_productPrice=ProductPriceForm(request.POST)
     frm_productImage=ProductImageForm(request.POST, request.FILES)

     if frm_productPrice.is_valid():
          product_price=frm_productPrice.save(commit=False)
          product_price.save()
          product_image=frm_productImage.save(commit=False)
          product_image.save()
          product=frm_product.save(commit=False)
          product.user=request.user
          product.pricing=product_price
          product.image=product_image
          product.save()
       
          return JsonResponse({'data':'ok'})
     else:
          print(frm_product.errors)
          print(frm_productPrice.errors)
          print(frm_productImage.errors)

          return JsonResponse({'data':frm_product.errors})
     

def get_products(request):
    try:
        g_product = Product.objects.select_related('image', 'pricing','user').values('prod_id','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image','user__username','user__first_name','user__last_name').filter(~Q(user__useraccount__usertype='ADMIN'),~Q(user__useraccount__usertype='SUPER ADMIN'))
        print(g_product)
        return JsonResponse(list(g_product), safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
def get_myproducts(request):
    try:
        g_product = Product.objects.select_related('image', 'pricing','user').values('prod_id','prod_status','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image','user__username','user__first_name','user__last_name').filter(user=request.user)
        print(g_product)
        return JsonResponse(list(g_product), safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
# def get_myproducts(request):
#     try:
#         if request.user.useraccount.usertype == 'ADMIN':
#             g_product = Product.objects.select_related('image', 'pricing').values('prod_id','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image').all()
#         else:
#             g_product = Product.objects.select_related('image', 'pricing').values('prod_id','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image').filter(user=request.user)

#         return JsonResponse(list(g_product), safe=False)
#     except Exception as e:
#         print(f"Error fetching Address data: {e}")
#         return JsonResponse({'error': str(e)}, status=500)
    
def get_client_products(request):
    
    try:
        g_product = Product.objects.select_related('image', 'pricing','user').values('prod_id','prod_status','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image','user__first_name','user__last_name').filter(prod_status='AVAILABLE')
        return JsonResponse(list(g_product), safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def get_singel_product(request):
    try:
        prod_id=request.POST.get('pid')
        # g_porduct=Product.objects.get(prod_id=prod_id)
        g_product = Product.objects.select_related('image', 'pricing', 'user').values('prod_id','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image','user__first_name','user__last_name','user__username').get(prod_id=prod_id)
     
        return JsonResponse(g_product, safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

def update_product(request):
    prod_id=request.POST.get('product_id')
    frm_product=ProductForm(request.POST)
    frm_productPrice=ProductPriceForm(request.POST)
    frm_productImage=ProductImageForm(request.POST, request.FILES)
    product = Product.objects.select_related("image","pricing").get(prod_id=prod_id)
    product.prod_name=request.POST.get('prod_name')
    product.prod_desc=request.POST.get('prod_desc')
    product.prod_category=request.POST.get('prod_category')
    product.save()
    product.pricing.p_qty=request.POST.get('p_qty')
    product.pricing.p_unit=request.POST.get('p_unit')
    product.pricing.p_price=request.POST.get('p_price')
    product.pricing.save()

    if request.FILES:
        product.image.pi_image=request.FILES.get('pi_image')
        product.image.save()

    return JsonResponse({'data':'ok'})

@csrf_exempt
def transfer_product(request):
    pid=request.POST.get('pid')
    g_admin=UserAccount.objects.select_related('user').get(usertype='ADMIN')
    tfrom=str(request.user.last_name)+','+str(request.user.first_name)
    try:
        gprod=Product.objects.select_related('pricing').get(prod_id=pid)
        gprod.user=g_admin.user
        gprod.save()

        th=TransferHistory(from_user=tfrom,to_user=g_admin,t_desc=gprod.prod_desc,t_qty=gprod.pricing.p_qty,t_product=gprod.prod_name,t_action='TRANSFER').save()
        return JsonResponse({'data':'ok'})
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

def cart_list(request):
    context={
            'page':'HOMEPAGE',
            'login_frm':LoginForm(),
            'signup_frm':SignUpForm()
        }

    return render(request,'storeapp/homepage/product_list.html',context)


@csrf_exempt
def delete_product(request):
    prod_id=request.POST.get('pid')
    Product.objects.get(prod_id=prod_id).delete()
    return JsonResponse({'data':'ok'})


def add_to_cart(request):
    pid=request.POST.get('pid')
    if request.user.is_anonymous:
        return JsonResponse({'data':'Please login to add product to cart'})
    else:
        chk_cart=Cart.objects.filter(Q(product__prod_id=pid) & Q(user=request.user)).count()
        if chk_cart > 0:
            return JsonResponse({'data':'Product already in cart'})
        else:
            product = Product.objects.select_related("image","pricing").get(prod_id=pid)
            try:
                cart=Cart.objects.create(product=product,user=request.user,cart_code=product.prod_name,cart_product_price=product.pricing.p_price,cart_unit=product.pricing.p_unit,cart_qty=1,cart_price=product.pricing.p_price).save()
                return JsonResponse({'data':'ok'})
            except Exception as e:
                print(f"Error fetching Address data: {e}")
                return JsonResponse({'error': str(e)}, status=500)

    

def cart_count(request):
    count=Cart.objects.filter(user=request.user).count()
    return JsonResponse(count, safe=False)

def mycart(request,user):
    address_subquery = Address.objects.filter(
            user=OuterRef('user'),
            ad_status='ACTIVE'
        ).annotate(
            full_address=Concat(
                'ad_lat',Value('-'),
                'ad_long',
                output_field=TextField()
            )
        ).values('full_address')[:1]
    g_admin = UserAccount.objects.select_related('user').values(
            'user__username',
            'user__first_name',
            'user__last_name',
            'usertype',
            'contact_no',
        ).annotate(
            address=Subquery(address_subquery)
        ).get(usertype='ADMIN')
    try:
        get_add=Address.objects.get(user=request.user, ad_status='ACTIVE')
        lat=get_add.ad_lat
        lng=get_add.ad_long
        ad_name=get_add.ad_name
    except Exception as e:
        lat=''
        lng=''
        ad_name=''
    print(g_admin)
    context={
          'page':'My CART',
          'lat':lat,
          'lng':lng,
          'add_name':ad_name,
          'admin':g_admin
       
     }
    json_data = json.dumps(context)
    return render(request,'storeapp/client/cart.html',{'json_data': json_data,'page':'MY CART'})


def get_cart_item(request):
    try:
        g_cart = Cart.objects.select_related('product','user').values('cart_id','product__prod_name','product__prod_desc','product__prod_category','product__pricing__p_qty','product__pricing__p_unit','product__pricing__p_price','product__image__pi_image','cart_unit','cart_qty','cart_price').filter(user=request.user)
        return JsonResponse(list(g_cart), safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def cart_update(request):
    cart_id=request.POST.get('cid')
    ttype=request.POST.get('ttype')
    try:
        cart=Cart.objects.get(cart_id=cart_id)
        if ttype == 'plus':
            cart.cart_qty=cart.cart_qty + 1
            cart.cart_price=cart.cart_product_price * cart.cart_qty
            cart.save()
        else:
            cart.cart_qty=cart.cart_qty - 1
            cart.cart_price=cart.cart_product_price * cart.cart_qty
            if cart.cart_qty == 0:
                cart.delete()
                return JsonResponse({'data':'Product removed from cart'})
            else:
                cart.save()
        
        return JsonResponse({'data':'ok'})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def searc_product(request):
    val=request.POST.get('sval')
    if request.user.useraccount.usertype == 'ADMIN':
        g_product = Product.objects.select_related('image', 'pricing').values('prod_id','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image').filter(Q(prod_name__icontains=val) | Q(prod_category__icontains=val))
    else:
        g_product = Product.objects.select_related('image', 'pricing').values('prod_id','prod_name','prod_desc','prod_category','pricing__p_qty','pricing__p_unit','pricing__p_price','image__pi_image').filter(Q(prod_name__icontains=val) | Q(prod_category__icontains=val),user=request.user)

    return JsonResponse(list(g_product), safe=False)

@csrf_exempt
def stat_product(request):
    prod_id=request.POST.get('pid')
    p_prod=Product.objects.get(prod_id=prod_id)
    p_prod.prod_status='AVAILABLE'
    p_prod.save()
    return JsonResponse({'data':'ok'})

@csrf_exempt
def search_user(request):
    val=request.POST.get('sval')
    address_subquery = Address.objects.filter(
            user=OuterRef('user'),
            ad_status='ACTIVE'
        ).annotate(
            full_address=Concat(
                'ad_name', Value(' - '),
                'ad_lat',Value(' - '),
                'ad_long',
                output_field=TextField()
            )
        ).values('full_address')[:1]

    g_user = UserAccount.objects.select_related('user').values(
            'user__id',
            'user__username',
            'user__first_name',
            'user__last_name',
            'usertype',
            'contact_no',
        ).annotate(
            address=Subquery(address_subquery)
        ).filter(Q(user__first_name__icontains=val) | Q(user__last_name__icontains=val) | Q(usertype__icontains=val), ~Q(usertype='ADMIN') , ~Q(usertype='SUPER ADMIN'))
    return JsonResponse(list(g_user), safe=False)


def get_users(request):
    try:
        address_subquery = Address.objects.filter(
            user=OuterRef('user'),
            ad_status='ACTIVE'
        ).annotate(
            full_address=Concat(
                'ad_name', Value(' - '),
                'ad_lat',Value(' - '),
                'ad_long',
                output_field=TextField()
            )
        ).values('full_address')[:1]

        g_user = UserAccount.objects.select_related('user').values(
            'user__id',
            'user__username',
            'user__first_name',
            'user__last_name',
            'usertype',
            'contact_no',
        ).annotate(
            address=Subquery(address_subquery)
        ).filter(~Q(usertype='ADMIN') & ~Q(usertype='SUPER ADMIN')).all()
        return JsonResponse(list(g_user), safe=False)
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    


def farmer_link(request,accesskey):
    context={
            'page':'FARMER_REGISTRATION',
            'login_frm':LoginForm(),
            'signup_frm':SignUpForm(),
            'address_frm':AddressForm()
        }

    return render(request,'storeapp/homepage/farmer_registration.html',context)

def farmer_address(request):
    context={
            'page':'FARMER_ADDRESS',
            'login_frm':LoginForm(),
            'signup_frm':SignUpForm(),
            'address_frm':AddressForm()
        }

    return render(request,'storeapp/homepage/farmer_address.html',context)


def get_orders(request):
    try:
        address_subquery = Address.objects.filter(
            user=OuterRef('user'),
            ad_status='ACTIVE'
        ).annotate(
            full_address=Concat(
                'ad_name', Value(' - '),
                'ad_lat',Value(' - '),
                'ad_long',
                output_field=TextField()
            )
        ).values('full_address')[:1]

        g_order = Order.objects.select_related('user').values('user__username','user__first_name','user__last_name','order_code','order_total','order_shipping','order_status','created_at').annotate(
            address=Subquery(address_subquery)
        ).all()
        # for o in g_order:
        #     print(g_order['created_at'])
        return JsonResponse(list(g_order), safe=False)
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)


url = "https://api.paymongo.com/v1/links"


@csrf_exempt
def cart_checkout(request):
    total=request.POST.get('total')
    ship=request.POST.get('ship')
    payment=request.POST.get('payment')
    code=order_code(8)
    tt=request.POST.get('total')
    try:
        tsub=tt.split('.')
        ttot=str(tsub[0])+'00'
    except Exception as e:
        tsub=tt
        ttot=str(tsub[0])+'00'

    print(ttot)
    try:
        ad_order=Order.objects.create(user=request.user,order_code=code,order_payment=payment,order_status='PENDING',order_total=total,order_shipping=ship).save()
        g_cart = Cart.objects.select_related('product','user').filter(user=request.user)
        cart=list(g_cart)
        for c in cart:
            gprod=Product.objects.get(prod_id=c.product.prod_id)
            OrderDetails.objects.create(user=request.user,od_code=code,product=gprod,od_prodname=c.product.prod_name,od_qty=c.cart_qty,od_unit=c.cart_unit,od_price=c.cart_price,od_status='PENDING').save()
            # r_cart=Cart.objects.get(product=c.product.prod_id, user=request.user).delete()
        if payment == 'Online Payment (GCASH)':
            payload = { "data": { "attributes": {
            "amount": int(ttot),
            "description": "VeggieCart Online Store",
            "remarks": "Online payment"
                    } } }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Basic c2tfdGVzdF9vd2VtYzM3eWZkZFVTeVppSHJQM2FFTEI6"
            }

            response = requests.post(url, json=payload, headers=headers).json()
            checkout_url = response['data']['attributes']['checkout_url']
            print(checkout_url)
            return JsonResponse({'data':'ok','checkout_url':checkout_url})
            # return HttpResponseRedirect(checkout_url)

        return JsonResponse({'data':'ok'})
    except Exception as e:
        print(f"Error fetching Address data: {e}")
        return JsonResponse({'error': str(e)}, status=500)

    

def checkout(request):

    

    payload = { "data": { "attributes": {
                "amount": 50000,
                "description": "VeggieCart",
                "remarks": "Online Payment"
            } } }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic c2tfdGVzdF9vd2VtYzM3eWZkZFVTeVppSHJQM2FFTEI6"
    }

    response = requests.post(url, json=payload, headers=headers).json()
    checkout_url = response['data']['attributes']['checkout_url']
    print(checkout_url)
    return HttpResponseRedirect(checkout_url)
