from django.urls import path
from . import views
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('create_fruit/', views.create_fruit, name='create_fruit'),
    path('fruit_edit/<int:fruta_id>/', views.fruit_edit, name='fruit_edit'),
    path('fruit_delete/<int:fruta_id>/', views.fruit_delete, name='fruit_delete'),
    path('create_seller/', views.create_seller, name='create_seller'),
    path('sale/<int:vendedor>/', views.sale, name='sale'),    
    path('relatorioVendedor/<int:vendedor>/', views.relatorioVendedor, name='relatorioVendedor'),    
    path('cadastro/', views.cadastro, name='cadastro'),
    path('calcular_valor_final/', views.calcular_valor_final, name='calcular_valor_final'),   
    
]
