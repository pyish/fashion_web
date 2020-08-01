from django.contrib import admin
from .models import Product, Category, OrderProduct, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category',)
    list_filter = ('category', 'rating')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'user', 'ordered_date', 'ordered')
    list_filter = ('ordered', 'ordered_date')
    search_fields = ('ref_code',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(OrderProduct)    