from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import DetailView
import logging

from . import models, forms, cart

logger = logging.getLogger(__name__)


def index(request):
    form = forms.SearchForm(request.POST or None)
    products = []
    n_pages = 12
    cart_obj = cart.Cart(request)

    if request.method == "GET":
        products = models.Product.objects.all().order_by('id')
        paginator = Paginator(products, n_pages)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        
        context = {
            "page_obj": page_obj,
            "form": form,
            "c_count": len(cart_obj),
        }
        return render(request, "shop/index.html", context)
    
    if request.method == "POST":
        if form.is_valid():
            search_term = form.cleaned_data.get("search")
            products = models.Product.objects.filter(title__icontains=search_term).order_by('id')
        
        paginator = Paginator(products, n_pages)
        page = request.POST.get("page")
        page_obj = paginator.get_page(page)
        
        context = {
            "page_obj": page_obj,
            "form": form,
        }
        return render(request, "shop/index.html", context)


class ProductDetail(DetailView):
    model = models.Product
    template_name = "shop/product_detail.html"


def checkout(request):
    form = forms.OrderForm(request.POST or None)
    cart_obj = cart.Cart(request)
    products = models.Product.objects.filter(pk__in=cart_obj.cart)
    total = products.aggregate(total=Sum("price"))["total"]
    context = {
        "form": form,
        "products": products,
        "total": total,
    }

    if products.exists():
        if request.method == "POST" and form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            instance.products.set(products)
            
            cart_obj.clear()

            return redirect("shop:index")
        return render(request, "shop/checkout.html", context)
    return redirect("shop:index")


def cart_view(request):
    if request.htmx:
        cart_obj = cart.Cart(request)
        logger.debug(f"cart.Cart content: {cart_obj.cart}")

        products = models.Product.objects.filter(pk__in=cart_obj.cart)
        total = products.aggregate(total=Sum("price"))["total"]
        context = {
            "products": products,
            "count": len(cart_obj),
            "total": total,
        }
        return render(request, "shop/cart.html", context)
    return redirect(request.path)


def cart_clear(request):
    if request.htmx:
        cart.Cart(request).clear()
        logger.debug(f"Clear cart content.")
        return HttpResponse(0)
    return redirect("shop:index")


def cart_add(request, pk):
    if request.htmx:
        cart_obj = cart.Cart(request)
        product = get_object_or_404(models.Product, pk=pk)
        cart_obj.add(product.pk)
        
        logger.debug(f"Add to cart: pk={product.pk}")
        logger.debug(f"cart.Cart content: {cart_obj.cart}")
        return HttpResponse(len(cart_obj))
    return redirect("shop:index")


def cart_remove(request, pk):
    if request.htmx:
        cart_obj = cart.Cart(request)
        product = get_object_or_404(models.Product, pk=pk)
        cart_obj.remove(product.pk)

        logger.debug(f"Remove from cart: pk={product.pk}")
        logger.debug(f"cart.Cart content: {cart_obj.cart}")
        return HttpResponse(len(cart_obj))
    return redirect("shop:index")
