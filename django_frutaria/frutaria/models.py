from django.db import models

class User(models.Model):
    nome = models.CharField(max_length=100)    
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)    

class Fruta(models.Model):
    nome = models.CharField(max_length=100)
    classificacao = models.CharField(max_length=100)
    fresca = models.BooleanField(default=True)
    qtd_estoque = models.IntegerField()
    preco = models.FloatField(default=0.00)

class Vendas(models.Model):
    fruta = models.ForeignKey(Fruta, on_delete=models.CASCADE)    
    qtd_vendida = models.IntegerField()
    vendedor_id = models.PositiveIntegerField()
    valor_venda = models.FloatField(default=0.00)
    data_venda = models.DateTimeField(auto_now_add=True)