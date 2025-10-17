from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from Products.views import ProductService, CategoryService, RawMaterialService, RawSupplierService, SupplierService, BatchService, PurchaseOrderService, PurchaseOrderDetailsService
import json
from Products.models import Supplier, RawMaterial
import datetime
import logging

logger = logging.getLogger(__name__)

# Instancias de las clases CRUD, sino no se pueden usar xd
product_service, category_service, raw_material_service, raw_supplier_service, supplier_service, batch_service,purchase_order_service, purchase_order_detail_service = ProductService(), CategoryService(), RawMaterialService(), RawSupplierService(), SupplierService(), BatchService(), PurchaseOrderService(),PurchaseOrderDetailsService()

@login_required
def dashboard(request):
    return render(request, 'main/dashboard.html')

#PRODUCTOSSSSSSSSSs
@login_required
def products_list(request):
    products = product_service.list()
    return render(request, 'main/products_list.html', {'products': products})

@login_required
def product_view(request, id):
    product = product_service.get(id)
    return render(request, 'main/product.html', {'p': product})

@login_required
def product_create(request):
    print("REQUEST METHOD:", request.method)  # <-- debug
    if request.method == 'POST':
        print("ENTRÓ EN POST")  # <-- debug
        success, form = product_service.save(request.POST)
        if success:
            return redirect('products_list')
        else:
            print(form.errors)
    else:
        form = product_service.form_class()
    
    return render(request, 'main/product_create.html', {'form': form})


@login_required
def product_update(request, id):
    if request.method == 'POST':
        success, form = product_service.update(id, request.POST)
        if success:
            return redirect('products_list')
    else:
        product = product_service.get(id)
        form = product_service.form_class(instance=product)
    
    return render(request, 'main/product_update.html', {'form': form})

@login_required
def product_delete(request, id):
        if request.method == 'GET':
            success = product_service.delete(id)
            if success:
                return redirect('products_list')
        return redirect('products_list') 

@login_required
def rawmaterial_list(request):
    rawmaterials = raw_material_service.list_actives()
    return render(request, 'main/rawmaterial_list.html',{'rawmaterials':rawmaterials})

@login_required
def rawmaterial_view(request, id):
    rawmaterial = raw_material_service.get(id)
    return render(request, 'main/rawmaterial.html', {'rawmaterial':rawmaterial})

@login_required
def rawmaterial_create(request):
    if request.method == 'POST':
        raw_material_form = raw_material_service.form_class(request.POST, prefix='material')
        raw_supplier_form = raw_supplier_service.form_class(request.POST, prefix='supplier')
        prices_form = raw_supplier_service.prices_form_class(request.POST, prefix='price')

        if raw_material_form.is_valid() and raw_supplier_form.is_valid() and prices_form.is_valid():
            success, raw_material = raw_material_service.save(raw_material_form.cleaned_data)
            if success:
                success2, raw_supplier = raw_supplier_service.save(raw_supplier_form.cleaned_data)
                if success2:
                    raw_supplier.fk_raw_material = raw_material
                    raw_supplier.save()
                    success3, price = raw_supplier_service.save_prices(
                        raw_supplier,
                        prices_form.cleaned_data.get('price'),
                        prices_form.cleaned_data.get('date')
                    )
                    if success3:
                        return redirect('rawmaterial_list')
                    else:
                        raw_supplier_service.delete(raw_supplier.id)
                        raw_material_service.delete(raw_material.id)
                else:
                    raw_material_service.delete(raw_material.id)
    else:
        raw_material_form = raw_material_service.form_class(prefix='material')
        raw_supplier_form = raw_supplier_service.form_class(prefix='supplier')
        prices_form = raw_supplier_service.prices_form_class(prefix='price')

    return render(request, 'main/rawmaterial_create.html', {
        'form': raw_material_form,
        'raw_supplier_form': raw_supplier_form,
        'prices_form': prices_form
    })

@login_required
def rawmaterial_update(request,id):
    if request.method == 'POST':
        success, form = raw_material_service.update(id, request.POST)
        if success:
            return redirect('rawmaterial_list')
    else:
        rawmaterial = raw_material_service.get(id)
        form = raw_material_service.form_class(instance=rawmaterial)
    return render(request,'main/rawmaterial_update.html',{'form':form, 'material':rawmaterial})

@login_required
def update_price(request, id):
    if request.method == 'POST':
        pass
    else:
        prices = raw_supplier_service.get(id)
        form = raw_supplier_service.prices_form_class(instance=prices)
    return render(request, 'main/update_prices.html', {'form': form, 'prices':prices})

@login_required
def rawmaterial_delete(request,id):
    if request.method == 'GET':
        success = raw_material_service.deactivate(id)
        if success:
            return redirect('rawmaterial_list')
    return redirect('rawmaterial_list')
        

#----------------- PROVEEDORES -----------------

@login_required
def supplier_list(request):
    suppliers = raw_supplier_service.get_data()
    print(suppliers)
    return render(request, 'main/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_view(request, id):
    supplier = supplier_service.get(id)
    return render(request, 'main/supplier.html', {'supplier':supplier})

@login_required
def supplier_create(request):
    print("REQUEST METHOD:", request.method)
    if request.method == 'POST':
        print("ENTRÓ EN POST")
        success, form = supplier_service.save(request.POST)
        if success:
            return redirect('supplier_list')
        else:
            print(form.errors)
    else:
        form = supplier_service.form_class()
    
    return render(request, 'main/supplier_create.html', {'form': form})

@login_required
def supplier_update(request, id):
    if request.method == 'POST':
        success, form = supplier_service.update(id, request.POST)
        if success:
            return redirect('supplier_list')
    else:
        supplier = supplier_service.get(id)
        form = supplier_service.form_class(instance=supplier)
    
    return render(request, 'main/supplier_update.html', {'form': form})

@login_required
def supplier_delete(request, id):
    if request.method == 'GET':
        success = supplier_service.delete(id)
        if success:
            return redirect('supplier_list')
    return redirect('supplier_list')

#pedidos
@login_required
def view_purchase_order(request):
    purchase_order_form = purchase_order_service.form_class()
    if request.method == 'POST':
        user = request.user
        supplier_info_json = request.POST.get('supplier_info')
        if supplier_info_json:
            supplier_info = json.loads(supplier_info_json)
            supplier = Supplier(
                id=supplier_info.get("id"),
                bussiness_name=supplier_info.get("bussiness_name"),
                rut=supplier_info.get("rut"),
                email=supplier_info.get("email"),
                phone=supplier_info.get("phone"),
                trade_terms=supplier_info.get("trade_terms")
            )

            raw_materials = []
            for key in request.POST:
                if key.startswith('raw_'):
                    try:
                        data = json.loads(request.POST[key])
                        quantity = int(data.get('quantity', 0))
                        price = float(data.get('price', 0))
                        if quantity > 0:
                            data['subtotal'] = price * quantity
                            raw_materials.append(data)
                    except json.JSONDecodeError:
                        return render(request, 'main/purchase_order.html', {'error': 'Error al procesar los datos del pedido.'})
            total_order = sum(float(item["price"]) * int(item["quantity"]) for item in raw_materials)
            context = {
                'supplier': supplier,
                'raw_materials': raw_materials,
                'total_order': total_order,
                'user': user,
                'form': purchase_order_form
            }
            print(context)
            return render(request, 'main/purchase_order.html', context)
        else:
            return render(request, 'main/purchase_order.html', {'error': 'No se encontró información del proveedor.'})
    else:
        return render(request, 'main/purchase_order.html', {'form': purchase_order_form})
    
@login_required
def purchase_order_confirm(request):
    if request.method == 'POST':
        supplier_info_json = request.POST.get('supplier_info')
        if not supplier_info_json:
            return render(request, 'main/purchase_order.html', {'error': 'No se encontró información del proveedor.'})
        
        supplier_info = json.loads(supplier_info_json)
        obj, created = Supplier.objects.get_or_create(
            rut=supplier_info.get("rut"),
            defaults={
                'bussiness_name': supplier_info.get("bussiness_name"),
                'email': supplier_info.get("email"),
                'phone': supplier_info.get("phone"),
                'trade_terms': supplier_info.get("trade_terms")
            }
        )
        purchase_order = purchase_order_service.model(
            supplier=obj,
            user=request.user.profile, 
            confirmation_date=request.POST.get('confirmation_date'),
            status=request.POST.get('status'),
            total_price=float(request.POST.get('total_price').replace(',', '.'))
        )
        purchase_order.save()
        today = datetime.date.today()

        for key in request.POST:
            if key.startswith('raw_'):
                try:
                    data = json.loads(request.POST[key])
                    data['stock_quantity'] = data['quantity']
                    date_str = data['expiration_date']
                    expiration_date = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
                    data['expiration_date'] = expiration_date
                    success, raw_obj = raw_material_service.save(data)
                    if success:
                        success2, raw_supplier = raw_supplier_service.create_raw_supplier(obj.id)
                        print("\n========== DEBUG purchase_order_confirm 2 ==========")
                        if success2:
                            print("\n========== DEBUG purchase_order_confirm 3 ==========")
                            raw_supplier.fk_raw_material = raw_obj.id
                            raw_supplier.save()
                            success3, price = raw_supplier_service.save_prices(
                                raw_supplier.id,
                                data['price'],
                                today
                            )
                            if success3:
                                print("\n========== DEBUG purchase_order_confirm 4 ==========")
                                purchase_order_details = {
                                    'purchase_order': purchase_order.id,
                                    'price_histories': price.id,
                                    'quantity': data['quantity'],
                                    'subtotal': data['subtotal']
                                }
                                success_purchase_detail, _ = purchase_order_detail_service.save(purchase_order_details)
                                if not success_purchase_detail:
                                    return render(request, 'main/purchase_order_confirm.html', {'error': '4'})
                            else:
                                return render(request, 'main/purchase_order_confirm.html', {'error': '3'})
                        else:
                            raw_supplier_service.delete(raw_supplier.id)
                            raw_material_service.delete(raw_obj.id)
                            return render(request, 'main/purchase_order_confirm.html', {'error': '2'})
                    else:
                        return render(request, 'main/purchase_order_confirm.html', {'error': raw_obj})
                except json.JSONDecodeError:
                    return render(request, 'main/purchase_order_confirm.html', {'error': 'Error al procesar los datos del pedido.', 'key':request.POST[key]})
        return redirect('suppliers_list')

    return render(request, 'main/purchase_order_confirm.html')


#BATCHSSSSSSSSSSSSSs

@login_required
def product_batch_list(request):
    batches = batch_service.list_products()
    return render(request, 'main/product_batch_list.html', {'batches': batches})

@login_required
def product_batch_view(request,id):
    if request.method == 'GET':
        batch = batch_service.get(id)
        prices = batch_service.price_model.objects.filter(batch__id=batch.id)
        return render(request, 'main/product_batch_view.html', {'batch': batch, 'prices': prices})
    else:
        return redirect('product_batch_list')
    

@login_required
def product_batch_create(request):
    form = batch_service.product_form_class()
    if request.method == 'POST':
        form = batch_service.product_form_class(request.POST)
        if form.is_valid():
            success, batch = batch_service.save_product_batch(form.cleaned_data)
            if success:
                data = {
                    'batch' : batch,
                    'price' : request.POST.get('price')
                }
                success2, price = batch_service.save_price(data)
                if success2:
                    return redirect('product_batch_list')
            else:
                return render(request, 'main/product_batch_create.html', {'form': batch})
    return render(request, 'main/product_batch_create.html', {'form': form})

@login_required
def product_batch_update(request, id):
    form = batch_service.product_form_class()
    if request.method == 'POST':
        success, obj = batch_service.update_product_batch(id, request.POST)
        if success:
            data = {
                    'batch' : obj,
                    'price' : request.POST.get('price')
                }
            success2, price = batch_service.save_price(data)
            if success2:
                return redirect('product_batch_list')
            else:
                print(data)
    else:
        batch = batch_service.get(id)
        form = batch_service.product_form_class(instance=batch)
        return render(request, 'main/product_batch_update.html', {'form': form})
    return render(request, 'main/product_batch_update.html', {'form': form})

@login_required
def product_batch_delete(request, id):
    if request.method == 'GET':
        success, obj = batch_service.delete_price(id)
        if success:
            success2 = batch_service.delete(id)
            if success2:
                return redirect('product_batch_list')
    return redirect('product_batch_list')

@login_required
def raw_batch_list(request):
    if request.method == 'POST':
        batches = batch_service.list_raw_materials()
        return render(request, 'main/raw_batch_list.html', {'batches': batches})
    else:
        return redirect('raw_batch_list')

@login_required
def raw_batch_create(request):
    form = batch_service.raw_form_class()
    if request.method == 'POST':
        form = batch_service.raw_form_class(request.POST)
        if form.is_valid():
            success, batch = batch_service.save_raw_batch(request.POST)
            if success:
                return redirect('raw_batch_list')
            else:
                return render(request, 'main/raw_batch_create.html', {'form': batch})
    return render(request, 'main/raw_batch_create.html', {'form': form})

@login_required
def raw_batch_update(request, id):
    if request.method == 'POST':
        success, form = batch_service.update_raw_batch(id, request.POST)
        if success:
            return redirect('raw_batch_list')
    else:
        batch = batch_service.get(id)
        form = batch_service.raw_form_class(instance=batch)
        return render(request, 'main/raw_batch_update.html', {'form': form})
    return render(request, 'main/raw_batch_update.html', {'form': form})

@login_required
def raw_batch_delete(request, id):
    if request.method == 'GET':
        success = batch_service.delete(id)
        if success:
            return redirect('raw_batch_list')
    return redirect('raw_batch_list')

#