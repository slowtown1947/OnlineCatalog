"""
URL configuration for PhoneCatalog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include

from phones import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('phones/', views.homepage, name='homepage'),
    path('page/<int:page>', views.homepage, name='paginator'),
    path('profile', views.user_profile_view, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('get_cart/', views.get_cart, name='get_cart'),
    path('delete_item_in_cart/', views.delete_item_in_cart, name='delete_item_in_cart'),
    path('plus_button_in_cart/', views.plus_button_in_cart, name='plus_button_in_cart'),
    path('minus_button_in_cart/', views.minus_button_in_cart, name='minus_button_in_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('finish_order/', views.finish_order, name='finish_order'),
    path('to_order/', views.to_order, name='to_order'),
    path('edit_page/', views.edit_page, name='edit_page'),
    path('order_done/<slug:bill_id>', views.confirm_order_non_register_user, name='confirm_order_non_register_user'),
    path('phone/<int:phone_id>/', views.view_phone, name='view_phone'),
    path('view_billing/<int:billing_id>/', views.view_billing, name='view_billing'),
    path('pages/<slug:page_url>', views.page_generator, name='page_generator'),
    path('phones/<slug:cat>', views.phone_category_brand, name='phone_category_brand'),
    path('search_goods', views.search_goods, name='search_goods'),

    path('test_view/', views.test_view, name='test_view'),


    # Auth
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # API
    path('api/', include('snippets.urls', namespace='snippets')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
