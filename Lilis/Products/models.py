from django.db import models

class Supplier(models.Model):
    bussiness_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    trade_terms = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.bussiness_name} - {self.rut}'
    
class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="products")
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expiration_date = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.sku}'
    
class RawSupplier(models.Model):
    fk_supplier = models.ForeignKey("Supplier", on_delete=models.PROTECT, related_name="raw_suppliers")
    fk_raw_material = models.ForeignKey("RawMaterial", on_delete=models.PROTECT, related_name="raw_materials")

    def __str__(self):
        return f'{self.fk_supplier} - {self.fk_raw_material}'

class PriceHistories(models.Model):
    fk_raw_supplier = models.ForeignKey("RawSupplier", on_delete=models.PROTECT, related_name="price_histories")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'{self.fk_raw_supplier.fk_raw_material.name} - {self.price} - {self.date}'

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    batch_code = models.CharField(max_length=100, unique=True)
    expiration_date = models.DateField()
    initial_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.batch_code}"
