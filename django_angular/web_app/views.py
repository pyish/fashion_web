from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product, Category, Order, OrderProduct
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q 

from users.forms import CheckoutForm, MpesaCodeForm
from users.models import Address,MpesaCode

import random
import string

all_products = Product.objects.all()
all_categories = Category.objects.all()

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def index(request):
    context = {
        'categories': all_categories,
        'products': all_products.filter(rating=0),
        'offer_products': all_products.filter(rating=1),
    }
    return render(request, 'web_app/index.html', context)

class Product_list(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'web_app/all_products.html'
    paginate_by = 3    

def product_detail(request, slug):
    product = all_products.get(slug=slug)
    category = product.category
    context = {
        'product': product,
        'related_products': all_products.filter(category__name=category, rating=0),
        'categories' : all_categories,
    }
    return render(request, 'web_app/product.html', context)

def categorydetail(request,pk):
    cat = Category.objects.get(pk = pk)
    
    context = {
        'products_with_category': Product.objects.filter(category__name = cat),
        'category' : cat,
        'categories' : all_categories,
        'cat_count': Product.objects.filter(category__name = cat).count(),
        'first2_prods': Product.objects.filter(category__name =cat)[:2], #Offer
        'four_prods': Product.objects.filter(category__name =cat)[2:],
        # 'other_four_prods': Product.objects.filter(category__name =cat)[6:10],
        # 'large_prod' :  Product.objects.filter(category__name =cat)[1],  
    }
    
    return render(request, 'web_app/category.html', context)

def offer_product(request):
    context = {
        'offer_prods' : all_products.filter(rating=1),
        'offer_count' : all_products.filter(rating=1).count()
    }
    return render(request, 'web_app/offer_products.html', context)
 

class SearchResultsView(View):
    def get(self, *args, **kwargs):
        qs =  Product.objects.all()
        query = self.request.GET.get('qproduct')        
        if query: 
            qs = qs.filter(Q(title__icontains=query))
            product_count = qs.count()
            if len(qs) == 0:
                messages.warning(self.request, f'No Product Named {query}')
                return redirect('/')
        elif query == '':
             messages.warning(self.request, 'No Product selected')
             return redirect('/')

        context = {
            'search_query_rslt' : qs,
            'product_count': product_count,
        }
        return render(self.request, 'web_app/search_results.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'categories' : all_categories,
            }
            return render(self.request, 'web_app/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect('/')

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, f'{order_product} quantity was updated.')
            return redirect('order-summary')
        else:
            order.products.add(order_product)
            messages.info(request, f'{order_product} was added to your cart.')
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date, ref_code=create_ref_code())
        order.products.add(order_product)
        messages.info(request, f'{order_product} was added to your cart.')
        return redirect('order-summary')

@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, f'{order_product} quantity was updated.')
            return redirect('order-summary')
        else:
            messages.info(request, f'{order_product} was not in your cart')
            return redirect('product', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.warning(request, f'{order_product} was removed from your cart.')
            return redirect('order-summary')
        else:
            messages.info(request, f'{order_product} was not in your cart')
            return redirect('product-detail', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product-detail', slug=slug)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            delivery_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if delivery_address_qs.exists():
                context.update(
                    {'default_delivery_address': delivery_address_qs[0]})

            return render(self.request, 'web_app/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order')
            return redirect('checkout')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_delivery = form.cleaned_data.get(
                    'use_default_delivery')
                if use_default_delivery:
                    print('Using the default delivery address')
                    address_qs = Address.objects.filter(
                        user=self.request.user,    
                        default=True
                    )
                    if address_qs.exists():
                        delivery_address = address_qs[0]
                        order.delivery_address = delivery_address
                        order.save()
                    else:
                        messages.info(
                            self.request, 'No default delivery address available')
                        return redirect('checkout')
                else:
                    print('User is entering a new delivery address')
                    delivery_address = form.cleaned_data.get(
                        'delivery_address')
                    mobi_number = form.cleaned_data.get(
                        'mobi_number')    

                    if is_valid_form([delivery_address, delivery_station, mobi_number]):
                        delivery_address = Address(
                            user=self.request.user,
                            delivery_address=delivery_address,
                            mobi_number=mobi_number
                        )
                        delivery_address.save()

                        order.delivery_address = delivery_address
                        order.save()

                        set_default_delivery = form.cleaned_data.get(
                            'set_default_delivery')
                        if set_default_delivery:
                            delivery_address.default = True
                            delivery_address.save()

                    else:
                        messages.info(
                            self.request, 'Please fill in the required delivery address field')
                        return redirect('checkout')
    
                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'M':
                    return redirect(reverse('fashion-home'))
                    #return redirect('payment', payment_option='Mpesa')
                elif payment_option == 'P':
                    print('Hey')
                    #self.request.session['order_id'] = order.id
                    #return redirect(reverse('payment:process'))
                    #messages.add_message(self.request, messages.INFO, 'Order Placed!')
                    #return redirect('checkout')
                else:
                    messages.warning(
                        self.request, 'Invalid payment option selected')
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order')
            return redirect('order-summary')


def payment_view(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'order': order
    }
    return render(request, 'web_app/payment.html', context)


def mpesa_code_view(request):
    form = MpesaCodeForm(request.POST or None)
    order = Order.objects.get(user=request.user, ordered=False)
    if form.is_valid():
        form.save()   
        order.ordered = True
        order.save()
        
        mpesa_code = form.cleaned_data.get('code')
        messages.info(request, f'Mpesa Code {mpesa_code} sent. You will be contacted shortly')
        return redirect('fashion-home')
    else:
        form = MpesaCodeForm()

    context = {
        'form':form
    }
    return render(request, 'web_app/mpesa_code.html', context)
