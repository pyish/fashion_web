from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


RATING = ((0, 'Product'), (1, 'Offer Product'))

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(default='fashion.jpg', upload_to='product_pics')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING, default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={
            'slug':self.slug
        })  

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            'slug': self.slug
        })          

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_ammount_saved(self):
        return self.get_total_product_price() - self.get_total_product_price

    def get_final_price(self):
        if self.product.discount_price:
            self.get_discount_product_price()
        return self.get_total_product_price()            

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()

        return total    












