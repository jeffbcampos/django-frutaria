from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Fruta, User, Vendas
from bcrypt import hashpw, gensalt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
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
            print(user.nome, user.password)       
            
            if hashpw(senha.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                if user.is_admin:
                    return render(request, 'admin.html') 
                else:
                    return redirect(reverse('sale', kwargs={'vendedor': user.id}))  
            else:
                return HttpResponse('Usuário ou senha inválidos!')
            
        except User.DoesNotExist:
            return HttpResponse('Usuário ou senha inválidos!')    

def cadastro(request):
    return render(request, 'cadastro.html')

    
@csrf_exempt
def create_user(request):
    data = request.POST
    nome = data.get('nome')
    password = data.get('password')
    role = data.get('role')
    
    if User.objects.filter(nome=nome).exists():
        messages.success(request, 'Usuário já existe!')
        return render(request, 'cadastro.html')
    
    is_admin = True if role == 'admin' else False
    
    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    user = User(nome=nome, password=hashed_password, is_admin=is_admin)
    user.save()
    messages.success(request, 'Usuário criado com sucesso!')
    return redirect('index')
    

@csrf_exempt
def create_fruit(request):
    if request.method == 'GET':
        frutas = Fruta.objects.all()
        # Passe 'frutas' para o contexto do template
        return render(request, 'create_fruit.html', {'frutas': frutas})
    
    if request.method == 'POST':
        data = request.POST
        nome = data.get('nome')
        classificacao = data.get('classificacao')
        fresca = True if data.get('fresca') == 'True' else False  # Corrigido para verificar 'True' em vez de 'on'
        qtd_estoque = data.get('qtd_estoque')
        preco = data.get('preco')            
        fruta = Fruta(nome=nome, classificacao=classificacao, fresca=fresca, qtd_estoque=qtd_estoque, preco=preco)
        fruta.save()
        messages.success(request, 'Fruta cadastrada!')        
        frutas = Fruta.objects.all()        
        return render(request, 'create_fruit.html', {'frutas': frutas})

@csrf_exempt    
def create_seller(request):
    return render(request, 'create_seller.html')

@csrf_exempt
def sale(request, vendedor):
    if request.method == 'GET':
        frutas = Fruta.objects.all()
        return render(request, 'vendedor.html', {'frutas': frutas, 'vendedor_id': vendedor})
    fruta_id = request.POST.get('fruta')    
    qtd_vendida = request.POST.get('quantidade')
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    venda = Vendas(fruta=fruta, vendedor_id=vendedor, qtd_vendida=qtd_vendida)
    venda.save()
    print(venda)
    messages.success(request, 'Venda realizada!')
    return render(request, 'vendedor.html', {'vendedor_id': vendedor})

@csrf_exempt
def relatorioVendedor(request, vendedor):    
    vendas = Vendas.objects.filter(vendedor_id=vendedor)
    # Renderiza um template, passando 'vendas' e 'vendedor' como contexto
    return render(request, 'relatorio_vendas.html', {'vendas': vendas, 'vendedor_id': vendedor})
    