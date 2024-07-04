from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .models import Fruta, User, Vendas
from bcrypt import hashpw, gensalt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.decorators.cache import never_cache

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
    if request.method == 'GET':
        users = User.objects.filter(is_admin=False)
        print(users)
        return render(request, 'cadastro.html', {'users': users})    

    
@csrf_exempt
def create_user(request):    
    if request.method == 'POST':
        data = request.POST
        nome = data.get('nome')
        password = data.get('password')
        role = data.get('role')
        
        if User.objects.filter(nome=nome).exists():
            messages.success(request, 'Usuário já existe!')
            return redirect('create_user')
        
        is_admin = True if role == 'admin' else False
        
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    
        user = User(nome=nome, password=hashed_password, is_admin=is_admin)
        user.save()
        messages.success(request, 'Usuário criado com sucesso!')
        return redirect('index')
    
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'GET':
        return render(request, 'edit_user.html', {'user': user})
    if request.method == 'POST':
        data = request.POST
        user.nome = data.get('nome')
        user.password = hashpw(data.get('password').encode('utf-8'), gensalt()).decode('utf-8')
        user.save()
        messages.success(request, 'Usuário atualizado!')
        return redirect('cadastro')
    
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'Usuário deletado!')
    return redirect('create_user')    

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
        fresca = True if data.get('fresca') == 'True' else False  
        qtd_estoque = data.get('qtd_estoque')
        preco = data.get('preco')            
        fruta = Fruta(nome=nome, classificacao=classificacao, fresca=fresca, qtd_estoque=qtd_estoque, preco=preco)
        fruta.save()
        messages.success(request, 'Fruta cadastrada!')        
        frutas = Fruta.objects.all()        
        return render(request, 'create_fruit.html', {'frutas': frutas})

def fruit_edit(request, fruta_id):
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    if request.method == 'GET':
        return render(request, 'edit_fruit.html', {'fruta': fruta})
    if request.method == 'POST':
        data = request.POST
        fruta.nome = data.get('nome')
        fruta.classificacao = data.get('classificacao')
        fruta.fresca = True if data.get('fresca') == 'True' else False
        fruta.qtd_estoque = data.get('qtd_estoque')
        fruta.preco = data.get('preco')
        fruta.save()
        messages.success(request, 'Fruta atualizada!')
        return redirect('create_fruit')

def fruit_delete(request, fruta_id):
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    fruta.delete()
    messages.success(request, 'Fruta deletada!')
    return redirect('create_fruit')

@csrf_exempt    
def create_seller(request):
    return render(request, 'create_seller.html')

@csrf_exempt
@never_cache
def sale(request, vendedor):
    if request.method == 'GET':
        frutas = Fruta.objects.filter(qtd_estoque__gt=0)        
        return render(request, 'vendedor.html', {'frutas': frutas, 'vendedor_id': vendedor})
    
    fruta_id = request.POST.get('fruta')    
    qtd_vendida = request.POST.get('quantidade')
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    desconto = request.POST.get('desconto', 0)
    
    # Diminuir a quantidade vendida da qtd_estoque da tabela fruta
    fruta.qtd_estoque -= int(qtd_vendida)
    fruta.save()
    
    venda = Vendas(fruta=fruta, vendedor_id=vendedor, qtd_vendida=qtd_vendida, valor_venda=calcular_valor(fruta_id, qtd_vendida, desconto))
    venda.save()
    
    messages.success(request, 'Venda realizada!')
    return render(request, 'vendedor.html', {'vendedor_id': vendedor, })

@csrf_exempt
def relatorioVendedor(request, vendedor):    
    vendas = Vendas.objects.filter(vendedor_id=vendedor)
    # Renderiza um template, passando 'vendas' e 'vendedor' como contexto
    return render(request, 'relatorio_vendas.html', {'vendas': vendas, 'vendedor_id': vendedor})

def calcular_valor_final(request):
    # Aqui você captura os valores enviados pelo HTMX
    fruta_id = request.GET.get('fruta')
    quantidade = request.GET.get('quantidade', 1)
    desconto = request.GET.get('desconto', 0)

    # Lógica para calcular o valor final com base nos parâmetros
    # Supondo que você tenha uma função que faça isso
    valor_final = calcular_valor(fruta_id, quantidade, desconto)

    # Retorna apenas o fragmento de HTML com o valor final
    return render(request, 'fragmentos/valor_final.html', {'valor_final': valor_final})

def calcular_valor(fruta_id, quantidade, desconto_decimal):
    # Busca a fruta pelo ID para obter o preço
    fruta = get_object_or_404(Fruta, pk=fruta_id)
    preco_fruta = fruta.preco

    # Converte quantidade para inteiro
    quantidade = int(quantidade)

    # Converte desconto para decimal (assumindo que já está em formato decimal)
    desconto_decimal = float(desconto_decimal)

    # Calcula o valor total sem desconto
    valor_total = preco_fruta * quantidade

    # Calcula o valor do desconto usando o valor decimal
    valor_desconto = valor_total * desconto_decimal

    # Calcula o valor final após aplicar o desconto
    valor_final = valor_total - valor_desconto
    
    valor_final_formatado = "{:.2f}".format(valor_final)
    print(valor_final_formatado)    

    return valor_final_formatado    