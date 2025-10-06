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

