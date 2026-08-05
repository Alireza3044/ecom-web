from django.contrib import admin
from .models import Product, Order

admin.site.site_title = "Ecom Web"
admin.site.site_header = "Ecom Web"
admin.site.index_title = "Manage Ecom Web"

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "discount_price", "category", "description"]
    search_fields = ["title", "price"]
    list_filter = ["price", "discount_price"]
    list_editable = ["price", "discount_price"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "address", "city", "state", "zipcode"]
    fields = ["name"]
    list_filter = ["city", "state"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
