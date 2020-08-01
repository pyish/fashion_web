from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fashion-home'),
    #path('about/', views.about, name='fashion-about'),
    path('full_menu/', views.Product_list.as_view(), name='fashion-menu'),
    #path('contact', views.contact, name='contact'),
    path('offer-products', views.offer_product, name='fashion-offers')

]