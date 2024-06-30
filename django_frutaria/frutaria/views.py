from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fruta, User, Vendas
from bcrypt import hashpw, gensalt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
import json

class IndexView(TemplateView):
    template_name = 'index.html'


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        try:
            user = User.objects.get(nome=usuario)
        except User.DoesNotExist:
            return HttpResponse('Usuário ou senha inválidos!')

        if user.password == hashpw(senha.encode('utf-8'), user.password.encode('utf-8')):
            if user.is_admin:
                return redirect('admin')  # ajuste a URL name conforme necessário
            else:
                return redirect('vendedor')  # ajuste a URL name conforme necessário
        else:
            return HttpResponse('Usuário ou senha inválidos!')    

    
@csrf_exempt
def create_user(request):
    data = json.loads(request.body)
    nome = data.get('nome')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    user = User(nome=nome, password=hashed_password, is_admin=is_admin)
    user.save()
    
    return JsonResponse({'message': 'Usuário criado com sucesso!'}, status=201)
    

@csrf_exempt
def create_fruit(request):
    data = json.loads(request.body)
    nome = data.get('nome')
    classificacao = data.get('classificacao')
    fresca = data.get('fresca')
    qtd_estoque = data.get('qtd_estoque')
    preco = data.get('preco')    
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
    