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
