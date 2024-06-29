from django.shortcuts import render
from django.http import HttpResponse
from .models import Fruta, User, Vendas
from bcrypt import hashpw, gensalt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def index(request):
    return HttpResponse('Olá, mundo!')
    
@csrf_exempt
def create_user(request):
    data = json.loads(request.body)    
    nome = data.get('nome')
    password = data.get('password')
    is_admin = data.get('is_admin')    
    print(nome, password, is_admin)    
    password = hashpw(password.encode('utf-8'), gensalt())
    user = User(nome=nome, password=password, is_admin=is_admin)    
    user.save()
    print(user)
    return HttpResponse('Usuário criado com sucesso!')

@csrf_exempt
def create_fruit(request):
    nome = request.POST.get('nome')
    classificacao = request.POST.get('classificacao')
    fresca = request.POST.get('fresca')
    qtd_estoque = request.POST.get('qtd_estoque')
    preco = request.POST.get('preco')
    fruta = Fruta(nome=nome, classificacao=classificacao, fresca=fresca, qtd_estoque=qtd_estoque, preco=preco)
    fruta.save()
    print(fruta)
    return HttpResponse('Fruta criada com sucesso!')

@csrf_exempt
def sale(request):
    fruta = request.POST.get('fruta')
    user = request.POST.get('user')
    qtd_vendida = request.POST.get('qtd_vendida')
    venda = Vendas(fruta=fruta, user=user, qtd_vendida=qtd_vendida)
    venda.save()
    print(venda)
    return HttpResponse('Venda realizada com sucesso!')

@csrf_exempt
def relatorioVendedor(request):
    user = request.POST.get('user')
    vendas = Vendas.objects.filter(user=user)
    return HttpResponse(vendas)
    