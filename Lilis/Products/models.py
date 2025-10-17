from django.db import models
from Accounts.models import Profile

class Supplier(models.Model):
    bussiness_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    trade_terms = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, default = 'Chile')
    currency = models.CharField(max_length=100, blank=True, default = 'CLP')
    status = models.CharField(max_length=20, choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A')

    def __str__(self):
        return f'{self.bussiness_name} - {self.rut}'
    
class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expiration_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

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
    uom_sells = models.CharField(max_length=100, choices=[('KG', 'Kilogramos'), ('UN', 'Unidades'), ('GR', 'Gramos')], default='UN')
    conversor_factor = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name} - {self.sku}'
    
class RawSupplier(models.Model):
    fk_supplier = models.ForeignKey("Supplier", on_delete=models.PROTECT, related_name="raw_suppliers")
    fk_raw_material = models.ForeignKey("RawMaterial", on_delete=models.PROTECT, related_name="raw_materials", null=True)

    def __str__(self):
        return f'{self.fk_supplier} - {self.fk_raw_material}'

class PriceHistories(models.Model):
    fk_raw_supplier = models.ForeignKey("RawSupplier", on_delete=models.PROTECT, related_name="price_histories", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=1.19)

    def __str__(self):
        return f'{self.fk_raw_supplier.fk_raw_material.name} - {self.price} - {self.date}'

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, null=True)
    batch_code = models.CharField(max_length=100, unique=True)
    expiration_date = models.DateField()
    initial_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    perishable = models.BooleanField(default=False)
    batch_control = models.BooleanField(default=False)
    serie_control = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.batch_code}"
    
class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="purchase_orders")
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="purchase_orders")
    created_at = models.DateField(auto_now_add=True)
    confirmation_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('P', 'Pendiente'), ('C', 'Confirmada'), ('A', 'Anulada')], default='P')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f'{self.status} - pedido: {self.id} - {self.supplier} - total: {self.total_price}'

    def total(self):
        total = sum(detail.subtotal() for detail in self.details.all())
        self.total_price = total
        self.save(update_fields=["total_price"])
        return total
    
class PurchaseOrderDetail(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="details")
    price_histories = models.ForeignKey(PriceHistories, on_delete=models.PROTECT, related_name="purchase_order_details")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.purchase_order.id} - {self.price_history.fk_raw_material.name} x {self.quantity} = {self.subtotal()}'

