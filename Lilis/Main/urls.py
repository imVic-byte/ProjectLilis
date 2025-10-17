from django.urls import path
from Main import views
list_products = [
    path('products_list/' , views.products_list ,name='products_list'),
    path('product_view<int:id>/', views.product_view, name='product_view'),
    path('product_create/' , views.product_create ,name='product_create'),
    path('product_delete/<int:id>/' , views.product_delete ,name='product_delete'),
    path('product_update/<int:id>/' , views.product_update ,name='product_update'),
]

list_raw_materials = [
    path('rawmaterial_list/', views.rawmaterial_list, name='rawmaterial_list'),
    path('rawmaterial_view/<int:id>/', views.rawmaterial_view, name='rawmaterial_view'),
    path('rawmaterial_create/', views.rawmaterial_create, name='rawmaterial_create'),
    path('rawmaterial_update/<int:id>/', views.rawmaterial_update, name='rawmaterial_update'),
    path('rawmaterial_delete/<int:id>/', views.rawmaterial_delete, name='rawmaterial_delete'),
    path('update_price/<int:id>/', views.update_price, name='update_price'),
]

list_suppliers = [
    path('supplier_list/', views.supplier_list, name='supplier_list'),
    path('supplier_view/<int:id>/', views.supplier_view, name='supplier_view'),
    path('supplier_create/', views.supplier_create, name='supplier_create'),
    path('supplier_update/<int:id>/', views.supplier_update, name='supplier_update'),
    path('supplier_delete/<int:id>/', views.supplier_delete, name='supplier_delete'),
]

list_users = [
    path("user_list/", views.user_list, name="user_list"),
    path("user_update/<int:id>/", views.user_update, name="user_update"),
    path("user_delete/<int:id>/", views.user_delete, name="user_delete"),
orders = [
    path('view_purchase_order/,', views.view_purchase_order, name='view_purchase_order'),
    path('purchase_order_confirm', views.purchase_order_confirm, name='purchase_order_confirm'),
]

batchs =[
    path('product_batch_list/', views.product_batch_list, name='product_batch_list'),
    path('product_batch_view/<int:id>/', views.product_batch_view, name='product_batch_view'),
    path('product_batch_create/', views.product_batch_create, name='product_batch_create'),
    path('product_batch_update/<int:id>/', views.product_batch_update, name='product_batch_update'),
    path('product_batch_delete/<int:id>/', views.product_batch_delete, name='product_batch_delete'),
]

urlpatterns = [
    path('dashboard/' , views.dashboard ,name='dashboard'),
    *list_products,
    *list_raw_materials,
    *list_suppliers,
    *list_users,
    *orders,
    *batchs,

]

