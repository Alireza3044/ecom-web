from django import forms
from .models import Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)


class OrderForm(forms.ModelForm):
    template_name = "shop/order_form_snippet.html"

    class Meta:
        model = Order
        fields = ["name", "email", "address", "city", "state", "zipcode"]
