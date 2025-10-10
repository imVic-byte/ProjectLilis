from django import forms
import datetime
from Products.models import Product, Category, Supplier, RawMaterial, RawSupplier, PriceHistories, Batch

class ProductForm(forms.ModelForm):
    expiration_date = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y'],  # formato dd-mm-yyyy
        widget=forms.DateInput(
            attrs={
                'type': 'text',           # text para poder escribir dd-mm-yyyy
                'placeholder': 'dd/mm/yyyy',
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'category', 'min_stock', 'max_stock', 'current_stock', 'expiration_date']
        labels = {
            'name': 'Nombre',
            'sku': 'Código SKU',
            'description': 'Descripción',
            'category': 'Categoría',
            'current_stock': 'Stock actual',
            'min_stock': 'Stock mínimo',
            'max_stock': 'Stock máximo',
            'expiration_date': 'Fecha de vencimiento',

        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Se requiere un nombre.')
        if len(name) < 2:
            raise forms.ValidationError('El nombre debe tener mas de 2 letras.')
        return name

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            raise forms.ValidationError('Se requiere un SKU.')
        if len(sku) < 3:
            raise forms.ValidationError('El SKU debe tener mas de 3 caracteres.')
        return sku

    def clean_min_stock(self):
        min_stock = self.cleaned_data.get('min_stock')
        if min_stock is None or min_stock < 0:
            raise forms.ValidationError('El stock minimo debe ser un numero positivo.')
        return min_stock
    
    def clean_max_stock(self):
        max_stock = self.cleaned_data.get('max_stock')
        if max_stock is None or max_stock < 0:
            raise forms.ValidationError('El stock maximo debe ser un numero positivo.')
        return max_stock
    
    def clean_current_stock(self):
        current_stock = self.cleaned_data.get('current_stock')
        if current_stock is None or current_stock < 0:
            raise forms.ValidationError('El stock actual debe ser un numero positivo.')
        return current_stock
    
    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date < datetime.date.today():
            raise forms.ValidationError("La fecha no puede ser pasada")
        return expiration_date
        
    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
        return product
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción'
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Se requiere un nombre.')
        if len(name) < 2:
            raise forms.ValidationError('El nombre debe tener mas de 2 letras.')
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 5:
            raise forms.ValidationError('La descripcion debe tener mas de 5 letras.')
        return description

    def save(self, commit=True):
        category = super().save(commit=False)
        if commit:
            category.save()
        return category

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['product', 'raw_material', 'batch_code', 'expiration_date', 'initial_quantity', 'current_quantity']
        label = {
            'product': 'Producto',
            'raw_material': 'Material',
            'batch_code': 'Codigo de lote',
            'expiration_date': 'Fecha de vencimiento',
            'initial_quantity': 'Cantidad inicial',
            'current_quantity': 'Cantidad actual',
        }
    def clean_batch_code(self):
        batch_code = self.cleaned_data.get('batch_code')
        if not batch_code:
            raise forms.ValidationError('Se requiere un codigo de lote.')
        if len(batch_code) < 3:
            raise forms.ValidationError('El codigo de lote debe tener mas de 3 caracteres.')
        return batch_code
    
    def clean_initial_quantity(self):
        initial_quantity = self.cleaned_data.get('initial_quantity')
        if initial_quantity is None or initial_quantity < 0:
            raise forms.ValidationError('La cantidad inicial debe ser un numero positivo.')
        return initial_quantity

    def clean_current_quantity(self):
        current_quantity = self.cleaned_data.get('current_quantity')
        initial_quantity = self.cleaned_data.get('initial_quantity')
        if current_quantity is None or current_quantity < 0:
            raise forms.ValidationError('La cantidad actual debe ser un numero positivo.')
        if initial_quantity is not None and current_quantity > initial_quantity:
            raise forms.ValidationError('La cantidad actual no puede ser mayor a la cantidad inicial.')
        return current_quantity 
    
    def clean_max_quantity(self):
        max_quantity = self.cleaned_data.get('max_quantity')
        if max_quantity is None or max_quantity < 0:
            raise forms.ValidationError('La cantidad maxima debe ser un numero positivo.')
        return max_quantity
    
    def clear_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        created_at = self.cleaned_data.get('created_at')
        if expiration_date < created_at:
            raise forms.ValidationError('La fecha de expiracion no puede ser anterior a la fecha de creacion.')
        
    def save(self, commit=True):
        batch = super().save(commit=False)
        if commit:
            batch.save()
        return batch
    
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['bussiness_name', 'rut', 'email', 'phone', 'trade_terms']
        labels = {
                'bussiness_name': 'Nombre de la empresa',
                'rut': 'RUT',
                'email': 'Correo electronico',
                'phone': 'Telefono',
                'trade_terms': 'Términos de comercio' 
                }
    def clean_bussiness_name(self):
        bussiness_name = self.cleaned_data.get('bussiness_name')
        if not bussiness_name:
            raise forms.ValidationError('Se requiere un nombre de empresa.')
        if len(bussiness_name) < 2:
            raise forms.ValidationError('El nombre de la empresa debe tener mas de 2 letras.')
        return bussiness_name

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise forms.ValidationError('Se requiere un RUT.')
        if len(rut) < 8:
            raise forms.ValidationError('El RUT debe tener mas de 8 caracteres.')
        return rut

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError('Ingrese un correo electronico valido.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 8:
            raise forms.ValidationError('El telefono debe tener mas de 8 caracteres.')
        return phone

    def save(self, commit=True):
        supplier = super().save(commit=False)
        if commit:
            supplier.save()
        return supplier

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ['name', 'description', 'stock_quantity', 'expiration_date']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'stock_quantity': 'Cantidad en stock',
            'expiration_date': 'Fecha de vencimiento' 
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Se requiere un nombre.')
        if len(name) < 2:
            raise forms.ValidationError('El nombre debe tener mas de 2 letras.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description) < 5:
            raise forms.ValidationError('La descripcion debe tener mas de 5 letras.')
        return description

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity is None or stock_quantity < 0:
            raise forms.ValidationError('La cantidad en stock debe ser un numero positivo.')
        return stock_quantity

    def save(self, commit=True):
        raw_material = super().save(commit=False)
        if commit:
            raw_material.save()
        return raw_material


    def save(self, commit=True):
        raw_supplier = super().save(commit=False)
        if commit:
            raw_supplier.save()
        return raw_supplier

class PriceHistoriesForm(forms.ModelForm):
    class Meta:
        model = PriceHistories
        fields = ['price', 'date']
        labels = {
            'price': 'Precio',
            'date': 'Fecha' 

        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 0:
            raise forms.ValidationError('El precio debe ser un numero positivo.')
        return price

    def save(self, commit=True):
        price_history = super().save(commit=False)
        if commit:
            price_history.save()
        return price_history

class RawSupplierForm(forms.ModelForm):
    class Meta:
        model = RawSupplier
        fields = ['fk_supplier']
        labels = {
            'fk_supplier': 'Proveedor' 
        }

    def clean_fk_supplier(self):
        fk_supplier = self.cleaned_data.get('fk_supplier')
        if not fk_supplier:
            raise forms.ValidationError('Se requiere un proveedor.')
        return fk_supplier

    def save(self, commit=True):
        raw_supplier = super().save(commit=False)
        if commit:
            raw_supplier.save()
        return raw_supplier




