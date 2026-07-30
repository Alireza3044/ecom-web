from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    products = models.ManyToManyField(Product, editable=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=5)


    def __str__(self):
        return self.name
