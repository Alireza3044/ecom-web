from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.ProductDetail.as_view(), name="detail"),
    path("cart/add/<int:product_pk>/", views.cart_add, name="cart-add"),
    path("cart/reduce/<int:product_pk>/", views.cart_reduce, name="cart-reduce"),
    path("cart/clear/", views.cart_clear, name="cart-clear"),
]
