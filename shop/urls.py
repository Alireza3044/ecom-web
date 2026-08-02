from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.ProductDetail.as_view(), name="detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("purchase-cancel/", views.purchase_cancel, name="purchase-cancel"),
    path("cart-count/", views.cart_count, name="cart-count"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/clear/", views.cart_clear, name="cart-clear"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart-add"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart-remove"),
]
