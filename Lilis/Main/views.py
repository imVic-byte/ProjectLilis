from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from Products.views import ProductService, CategoryService, RawMaterialService, RawSupplierService, SupplierService, BatchService, PurchaseOrderService
import json
from Products.models import Supplier

# Instancias de las clases CRUD, sino no se pueden usar xd
product_service, category_service, raw_material_service, raw_supplier_service, supplier_service, batch_service,purchase_order_service = ProductService(), CategoryService(), RawMaterialService(), RawSupplierService(), SupplierService(), BatchService(), PurchaseOrderService(),

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
    if request.method == 'POST':
        purchase_order_form = purchase_order_service.form_class()
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
            return render(request, 'main/purchase_order.html', context)
        else:
            return render(request, 'main/purchase_order.html', {'error': 'No se encontró información del proveedor.'})
    else:
        return render(request, 'main/purchase_order.html')
