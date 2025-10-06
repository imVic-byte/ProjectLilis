from django.contrib import admin
from Products.models import Product, Category, Supplier, RawMaterial, RawSupplier, PriceHistories
from Accounts.models import Profile, Role, RoleModulePermission
from Sells.models import Client, Location, Warehouse

def makeActive(modeladmin, request, queryset):
    queryset.update(is_active=True)
class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('name','sku','current_stock', 'min_stock', 'max_stock','description')
    show_change_link = True
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [ProductInline,]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'category', 'current_stock', 'min_stock', 'max_stock')
    search_fields = ('name', 'sku')
    list_filter = ('category',)
    ordering = ('name',)
    list_select_related = ('category',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('bussiness_name', 'rut', 'email', 'phone')
    search_fields = ('bussiness_name', 'rut', 'email', 'phone')
    ordering = ('bussiness_name',)

@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stock_quantity', 'expiration_date')
    search_fields = ('name',)
    ordering = ('name',)
@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module', 'can_view', 'can_add', 'can_edit', 'can_delete')
    list_filter = ('role', 'module')
    search_fields = ('role__name', 'module__name')
    ordering = ('role__name', 'module__name')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'run', 'phone', 'role')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'run', 'phone', 'role__name')
    list_filter = ('role',)
    ordering = ('user__username',)
    list_select_related = ('user', 'role')
    actions = [makeActive]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('bussiness_name', 'rut', 'email', 'credit_limit', 'max_debt', 'is_suspended')
    search_fields = ('bussiness_name', 'rut', 'email')
    list_filter = ('is_suspended',)
    ordering = ('bussiness_name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')
    ordering = ('name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_area', 'location')
    search_fields = ('name', 'address', 'location__name')
    list_filter = ('location',)
    ordering = ('name',)
    list_select_related = ('location',)
    
@admin.register(RawSupplier)
class RawSupplier(admin.ModelAdmin):
    list_display = ('fk_supplier', 'fk_raw_material')
    search_fields = ('fk_supplier__bussiness_name', 'fk_raw_material__name')
    list_filter = ('fk_supplier',)
    ordering = ('fk_supplier__bussiness_name',)
    list_select_related = ('fk_supplier', 'fk_raw_material')

@admin.register(PriceHistories)
class PriceHistoriesAdmin(admin.ModelAdmin):
    list_display = ('fk_raw_supplier', 'price', 'date')
    search_fields = ('fk_raw_supplier__fk_supplier__bussiness_name', 'fk_raw_supplier__fk_raw_material__name')
    list_filter = ('date',)
    ordering = ('-date',)
    list_select_related = ('fk_raw_supplier', 'fk_raw_supplier__fk_supplier', 'fk_raw_supplier__fk_raw_material')