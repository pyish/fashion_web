"""django_angular URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from users import views as user_views
from django.conf.urls.static import static
from django.urls import path, include

from web_app.views import (
    product_detail,
    categorydetail,
    SearchResultsView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_product_from_cart,
    CheckoutView,
    payment_view,
    mpesa_code_view,
)


urlpatterns = [
    path('', include('web_app.urls')),
    path('admin/', admin.site.urls),
    
    #products urls
    path('product/<slug:slug>', product_detail, name='product-detail'),
    path('categorys/<int:pk>/', categorydetail, name='category-detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('users/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='fashion-register'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-product-from-cart/<slug:slug>/', remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment-details', payment_view, name='payment'),
    path('mpesa-code/', mpesa_code_view, name='mpesa-code')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)