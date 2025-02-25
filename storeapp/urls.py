from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('auth_user',views.auth_user,name='auth_user'),
    path('signup',views.signup,name='signup'),
    path('signout',views.signout,name='signout'),
    path('homepage',views.homepage,name='homepage'),
    path('profile',views.profile,name='profile'),
    path('cart/<str:user>',views.cart,name='cart'),
    path('mycart/<str:user>',views.mycart,name='mycart'),
    path('save_address',views.save_address,name='save_address'),
    path('up_address',views.up_address,name='up_address'),
    path('get_address/',views.get_address,name='get_address'),
    path('add_product',views.add_product,name='add_product'),
    path('get_products/',views.get_products,name='get_products'),
    path('get_myproducts/',views.get_myproducts,name='get_myproducts'),
    path('get_client_products/',views.get_client_products,name='get_client_products'),
    path('get_singel_product',views.get_singel_product,name='get_singel_product'),
    path('update_product',views.update_product,name='update_product'),
    path('products',views.cart_list,name='cart_list'),
    path('delete_product',views.delete_product,name='delete_product'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart_count/',views.cart_count,name='cart_count'),
    path('get_cart_item/',views.get_cart_item,name='get_cart_item'),
    path('cart_update',views.cart_update,name='cart_update'),
    path('searc_product',views.searc_product,name='searc_product'),
    path('get_users/',views.get_users,name='get_users'),
    path('search_user',views.search_user,name='search_user'),
    path('farmer/reg/<str:accesskey>',views.farmer_link,name="farmer_link"),
    path('farmer_address',views.farmer_address,name='farmer_address'),
    path('checkout',views.checkout,name='checkout'),
    path('transfer_product',views.transfer_product,name='transfer_product'),
    path('stat_product',views.stat_product,name='stat_product'),
    path('cart_checkout',views.cart_checkout,name='cart_checkout'),
    path('get_orders/',views.get_orders,name='get_orders'),

    # farmer
    path('get_myproducts',views.get_myproducts,name='get_myproducts'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)