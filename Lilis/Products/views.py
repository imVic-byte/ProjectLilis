from Products.models import (
    Product, Category, RawMaterial, Batch, Supplier, 
    RawSupplier, PriceHistories, 
)
from Products.forms import (
    RawMaterialForm, RawSupplierForm, PriceHistoriesForm, BatchForm, ProductForm, 
    CategoryForm, SupplierForm
)


class CRUD:
    def get(self, id):
        try:
            return self.model.objects.get(id=id)
        except self.model.DoesNotExist:
            return None

    def list(self):
        return self.model.objects.all()

    def delete(self, id):
        try:
            instance = self.model.objects.get(id=id)
            instance.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def save(self, data):
        form = self.form_class(data)
        if form.is_valid():
            obj = form.save()
            return True, obj
        return False, form

    def update(self, id, data):
        try:
            instance = self.model.objects.get(id=id)
            form = self.form_class(data, instance=instance)
            if form.is_valid():
                form.save()
                return True, form
            return False, form
        except self.model.DoesNotExist:
            return False, None
        
    def search_by_name(self, name):
        return self.model.objects.filter(name__icontains=name)
    
    def count(self):
        return self.model.objects.count()

class CategoryService(CRUD):
    def __init__(self):
        self.model = Category
        self.form_class = CategoryForm
    
    def filter_by_category(self, category_id):
        category = self.model.objects.filter(id=category_id).first()
        if category:
            return category.products.all()
        return self.model.objects.none()
    

class ProductService(CRUD):
    def __init__(self):
        self.model = Product
        self.form_class = ProductForm
    
    def search_by_sku(self, sku):
        return self.model.objects.filter(sku=sku).first()
    
    def search_by_description(self, description):
        return self.model.objects.filter(description__icontains=description)
    
class SupplierService(CRUD):
    def __init__(self):
        self.model = Supplier
        self.form_class = SupplierForm
    
    def search_by_rut(self, rut):
        return self.model.objects.filter(rut=rut).first()
    
    def search_by_trade_terms(self, trade_terms):
        return self.model.objects.filter(trade_terms__icontains=trade_terms)
    
    
class RawMaterialService(CRUD):
    def __init__(self):
        self.model = RawMaterial
        self.form_class = RawMaterialForm
    
    def search_by_description(self, description):
        return self.model.objects.filter(description__icontains=description)


class RawSupplierService(CRUD):
    def __init__(self):
        self.model = RawSupplier
        self.prices = PriceHistories
        self.form_class = RawSupplierForm
        self.prices_form_class = PriceHistoriesForm

    def create_raw_supplier(self,data):
        form = self.form_class(data)
        if form.is_valid():
            raw_supplier = form.save()
            return True, raw_supplier
        return False, form

    def save_prices(self, raw_supplier, price, date):
        data = {'fk_raw_supplier':raw_supplier, 'price': price, 'date': date}
        print("_________________________________")
        print(data)
        print("_________________________________")
        form = self.prices_form_class(data)
        if form.is_valid():
            obj = form.save(data)
            obj.fk_raw_supplier = data['fk_raw_supplier']
            obj.save()
            return True, obj
        return False, obj

    def search_by_supplier(self, supplier_id):
        return self.model.objects.filter(fk_supplier__id=supplier_id)
    
    def search_by_raw_material(self, raw_material_id):
        return self.model.objects.filter(fk_raw_material__id=raw_material_id)
    
    def search_by_both(self, supplier_id, raw_material_id):
        return self.model.objects.filter(fk_supplier__id=supplier_id, fk_raw_material__id=raw_material_id).first()
    
    def list_prices(self, raw_supplier_id):
        raw_supplier = self.model.objects.filter(id=raw_supplier_id).first()
        if raw_supplier:
            return self.prices.objects.filter(fk_raw_supplier=raw_supplier)
        return self.prices.objects.none()

class BatchService(CRUD):
    def __init__(self):
        self.model = Batch
        self.form_class = BatchForm

    def search_by_product(self, product_id):
        return self.model.objects.filter(product__id=product_id)
    
    def search_by_raw_material(self, raw_material_id):
        return self.model.objects.filter(raw_material__id=raw_material_id)
    
    def list_products(self):
        return self.model.objects.filter(product__isnull=False)
    
    def list_raw_materials(self):
        return self.model.objects.filter(raw_material__isnull=False)