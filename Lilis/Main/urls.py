from django.urls import path
from Main import views

urlpatterns = [
    path('dashboard/' , views.dashboard ,name='dashboard'),
    path('products_list/' , views.products_list ,name='products_list'),
    path('product_view<int:id>/', views.product_view, name='product_view'),
    path('product_create/' , views.product_create ,name='product_create'),
    path('product_delete/<int:id>/' , views.product_delete ,name='product_delete'),
    path('product_update/<int:id>/' , views.product_update ,name='product_update'),
    path('rawmaterial_list/', views.rawmaterial_list, name='rawmaterial_list'),
    path('rawmaterial_view/<int:id>/', views.rawmaterial_view, name='rawmaterial_view'),
    path('rawmaterial_create/', views.rawmaterial_create, name='rawmaterial_create'),
    path('rawmaterial_update/<int:id>/', views.rawmaterial_update, name='rawmaterial_update'),
    path('rawmaterial_delete/<int:id>/', views.rawmaterial_delete, name='rawmaterial_delete'),
    path('supplier_list/', views.supplier_list, name='supplier_list'),
    path('supplier_view/<int:id>/', views.supplier_view, name='supplier_view'),
    path('supplier_create/', views.supplier_create, name='supplier_create'),
    path('supplier_update/<int:id>/', views.supplier_update, name='supplier_update'),
    path('supplier_delete/<int:id>/', views.supplier_delete, name='supplier_delete'),
]