from django.db import models
from Products.models import Batch
from Accounts.models import Profile

class Client(models.Model):
    bussiness_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bussiness_name} - {self.rut}'
    
class Location (models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    total_area = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.ForeignKey("Location", on_delete=models.PROTECT, related_name="warehouses")

    def __str__(self):
        return f'{self.name} - {self.location.name}'
    
class WareClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="client")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="warehouses")
    status = models.CharField(max_length=20, choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A')
    association_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client.bussiness_name} - {self.warehouse.name} - status: {self.status}'
    

class Transaction(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="warehouse")
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name="bash")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="transactions")
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=[('I', 'Ingreso'), ('S', 'Salida')], default='I')

    def __str__(self):
        return f'{self.type} - Lote: {self.bash.name} - hacia bodega: {self.warehouse.name} - con fecha: {self.date}'
    

class SaleOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="sale_orders")
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="sale_orders")
    created_at = models.DateField(auto_now_add=True)
    confirmation_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('P', 'Pendiente'), ('C', 'Confirmada'), ('A', 'Anulada')], default='P')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.status} - pedido de: {self.client.bussiness_name} - con fecha: {self.created_at} contenido:'
    
    def total(self):
        total = sum(detail.subtotal() for detail in self.details.all())
        self.total_price = total
        self.save(update_fields=["total_price"])
        return total

class BatchPriceHistory(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name="batch_price_histories")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.batch.name} - {self.price} - {self.date}'

class SaleOrderDetail(models.Model):
    sale_order = models.ForeignKey(SaleOrder, on_delete=models.PROTECT, related_name="details")
    price_histories = models.ForeignKey(BatchPriceHistory, on_delete=models.PROTECT, related_name="order_details")
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def subtotal(self):
        subtotal = self.price_histories.price * self.quantity
        self.subtotal = subtotal
        self.save(update_fields=["subtotal"])
        return subtotal
    
    def __str__(self):
        return f'{self.sale_order.id} - {self.price_histories.batch.batch_code} x {self.quantity} = {self.subtotal()}'


