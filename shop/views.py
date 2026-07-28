from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import DetailView
from .models import Product
from .forms import SearchForm
from .cart import Cart
import logging

logger = logging.getLogger(__name__)


def index(request):
    form = SearchForm(request.POST or None)
    products = []
    n_pages = 12
    cart = Cart(request)

    if request.method == "GET":
        products = Product.objects.all().order_by('id')
        paginator = Paginator(products, n_pages)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)
        
        context = {
            "page_obj": page_obj,
            "form": form,
            "c_count": len(cart),
        }
        return render(request, "shop/index.html", context)
    
    if request.method == "POST":
        if form.is_valid():
            search_term = form.cleaned_data.get("search")
            products = Product.objects.filter(title__icontains=search_term).order_by('id')
        
        paginator = Paginator(products, n_pages)
        page = request.POST.get("page")
        page_obj = paginator.get_page(page)
        
        context = {
            "page_obj": page_obj,
            "form": form,
        }
        return render(request, "shop/index.html", context)


class ProductDetail(DetailView):
    model = Product
    template_name = "shop/product_detail.html"


def cart_add(request, product_pk):
    if request.htmx:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_pk)
        cart.add(product.pk)
        
        logger.debug(f"Add to cart: id={product.pk}")
        logger.debug(f"Cart content: {cart.get_cart()}")
        return HttpResponse(len(cart))
    return redirect("shop:index")


def cart_reduce(request, product_pk):
    if request.htmx:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_pk)
        cart.reduce(product.pk)

        logger.debug(f"Reduce from cart: id={product.pk}")
        logger.debug(f"Cart content: {cart.get_cart()}")
        return HttpResponse(len(cart))
    return redirect("shop:index")


def cart_clear(request):
    if request.htmx:
        Cart(request).clear()
        logger.debug(f"Clear cart content.")
        return HttpResponse(0)
    return redirect("shop:index")
