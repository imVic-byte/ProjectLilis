from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from Products.views import ProductService, CategoryService, RawMaterialService, RawSupplierService, SupplierService, BatchService

# Instancias de las clases CRUD, sino no se pueden usar xd
product_service, category_service, raw_material_service, raw_supplier_service, supplier_service, batch_service = ProductService(), CategoryService(), RawMaterialService(), RawSupplierService(), SupplierService(), BatchService()

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
    rawmaterials = raw_material_service.list()
    return render(request, 'main/rawmaterial_list.html',{'rawmaterials':rawmaterials})

@login_required
def rawmaterial_view(request, id):
    rawmaterial = raw_material_service.get(id)
    return render(request, 'main/rawmaterial.html', {'rawmaterial':rawmaterial})

@login_required
def rawmaterial_create(request):
    raw_material_form = raw_material_service.form_class()
    raw_supplier_form = raw_supplier_service.form_class()
    prices_form = raw_supplier_service.prices_form_class()
    if request.method == 'POST':
        success, raw_material_obj = raw_material_service.save(request.POST)
        if success:
            success2, raw_supplier_obj = raw_supplier_service.create_raw_supplier(request.POST)
            if success2:
                raw_supplier_obj.fk_raw_material = raw_material_obj
                raw_supplier_obj.save()
                success3, prices_obj = raw_supplier_service.save_prices(raw_supplier_obj, request.POST.get('price'), request.POST.get('date'))
                if success3:
                    return redirect('rawmaterial_list')
                else:
                    print(prices_obj.errors)
            else:
                print(raw_supplier_obj.errors)
        else:
            print(raw_material_obj.errors)
    return render(request, 'main/rawmaterial_create.html', {'form':raw_material_form, 'raw_supplier_form':raw_supplier_form, 'prices_form':prices_form})

@login_required
def rawmaterial_update(request,id):
    if request.method == 'POST':
        success, form = raw_material_service.update(id, request.POST)
        if success:
            return redirect('rawmaterial_list')
    else:
        rawmaterial = raw_material_service.get(id)
        form = raw_material_service.form_class(instance=rawmaterial)
    return render(request,'main/rawmaterial_update.html',{'form':form})

@login_required
def rawmaterial_delete(request,id):
    if request.method == 'GET':
        success = raw_material_service.delete(id)
        if success:
            return redirect('rawmaterial_list')
    return redirect('rawmaterial_list')
        

#----------------- PROVEEDORES -----------------

@login_required
def supplier_list(request):
    suppliers = supplier_service.list()
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