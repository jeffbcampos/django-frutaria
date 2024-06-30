from django.urls import path
from . import views
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_fruit/', views.create_fruit, name='create_fruit'),
    path('sale/', views.sale, name='sale'),
    path('relatorioVendedor/', views.relatorioVendedor, name='relatorioVendedor'),
]
