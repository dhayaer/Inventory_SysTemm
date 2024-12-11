from django.db import models
import uuid
from versatileimagefield.fields import VersatileImageField
from django.db import models


# Product model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.BigIntegerField(unique=True)
    product_code = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    product_image = VersatileImageField(upload_to="uploads/", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_user = models.ForeignKey("auth.User", related_name="user%(class)s_objects", on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    hsn_code = models.CharField(max_length=255, blank=True, null=True)
    total_stock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "products_product"
        unique_together = (("product_code", "product_id"),)
        ordering = ("-created_date", "product_id")
        abstract = True

    def _str_(self):
        return self.product_name

# Variant model
class Variant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Make sure Product is correctly referenced
    variant_name = models.CharField(max_length=255)
    variant_price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return self.name

# SubVariant model
class SubVariant(models.Model):
    variant = models.ForeignKey(Variant, related_name="subvariants", on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    stock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8)

    def _str_(self):
        return f"{self.variant.name}: {self.option}"
    
class Product(models.Model):
    name = models.CharField(max_length=255)  # Name of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product

    def __str__(self):
        return self.name