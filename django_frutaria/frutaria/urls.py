from django.urls import path
from . import views
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_fruit/', views.create_fruit, name='create_fruit'),
    path('create_seller/', views.create_seller, name='create_seller'),
    path('sale/<int:vendedor>/', views.sale, name='sale'),
    path('relatorioVendedor/<int:vendedor>/', views.relatorioVendedor, name='relatorioVendedor'),    
    path('cadastro/', views.cadastro, name='cadastro'),   
    
]
