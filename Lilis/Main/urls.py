from django.urls import path
from Main import views

urlpatterns = [
    path('dashboard' , views.dashboard ,name='dashboard'),
    path('products_list' , views.products_list ,name='products_list'),
    path('product_view<int:id>/', views.product_view, name='product_view'),
    path('product_create' , views.product_create ,name='product_create'),
    path('product_delete<int:id>' , views.product_delete ,name='product_delete'),
    path('product_update<int:id>' , views.product_update ,name='product_update'),
]