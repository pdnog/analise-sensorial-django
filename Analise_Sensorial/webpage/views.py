from django.shortcuts import render, redirect
from webpage.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from webpage.models import *
from webpage.utilitarios import confirmacao_cadastro
from django.http import HttpResponse

# Create your views here.
#Jogando o formulário para o html

#Iniciando a classe
_confirmacao = confirmacao_cadastro()

def Inicio(request):
	return render(request, "home.html")

def Fabricante_page_cadastro(request):
	form = FormFabricante()
	return render(request, "Fabricante.html", {"form":form})

def Provador_page_cadastro(request):
	form = FormProvador()
	return render(request, "Provador.html", {"form":form})

def Cadastro_principal_page(request):
	return render(request, "cadastro_principal.html")

#Cadastrando um fabricante
def Cadastro_Fabricante(request):
	if request.method == 'POST':
		form = FormFabricante(request.POST)
		#Vendo se o formário com o resquest é válido, se for, ele salva no models, pois o form é uma extensão do model
		if form.is_valid():
			form.save()
			#Retornando o usuário do formulario
			username = form.cleaned_data['username']
			#Retornando o objeto usuário
			usuario = User.objects.get(username=username)
			#Definindo o tipo de usuário pelo ID
			tipagem = Tipagem.objects.create(user_id=usuario.id, tipo='F')
			#Setando "True" ao parametro da classe
			_confirmacao.setConfirmacao(True)
			#Redirecionando para a página principal
			return redirect("/")
	else:
		#Se o método não for POST, ele mostra um formulário em branco
		form = FormFabricante()
	return render(request, "Fabricante.html", {"form":form})

#Cadastrando um provador
def Cadastro_Provador(request):
	if request.method == 'POST':
		#Tenho que fazer o tratamento de erros na view!!!
		form = FormProvador(request.POST)
		#Verificando se o formulário é válido
		if form.is_valid():
			form.save()
			#Retornando o usuário
			username = form.cleaned_data['username']
			#Retornando o objeto usuário
			usuario = User.objects.get(username=username)
			#Definindo o tipo de usuário
			tipagem = Tipagem.objects.create(user_id=usuario.id, tipo='P')
			#Setando "True" ao parametro da classe
			_confirmacao.setConfirmacao(True)
			#Redirecionando para a página principal
			return redirect("/")
	else:
		form = FormProvador()

	return render(request, "Provador.html", {"form":form})

#Pagina de Login
def Login_Page(request):
	form = FormLogin()
	#Variável que irá para o template
	confirm = False
	if(_confirmacao.getConfirmacao()):
		#Recebendo o valor
		confirm = True
		_confirmacao.setConfirmacao(False)
	else:
		#Quando o usuário recarregar a página, a mensagem não estará mais lá
		confirm = False

	return render(request, "Login.html", {"form":form, "confirmacao":confirm})

#Fazendo login
def Login(request):

	#Recebendo o formulário preenchido
	form = FormLogin(request.POST)
	#Validando o formullário
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		#Autenticando o usuário no sistema
		user = authenticate(username=username, password=password)
		#Conferindo se existe o usuário
		if user is not None:
			user = User.objects.get(username=username)
			#Recuperando o tipo do usuário
			tipo = Tipagem.objects.get(user_id=user.id)

			#Logando e fazendo o backend do usuario
			if user.is_active:
				#Retornando o arquivo settings para o caminho do backend
				user.backend = settings.AUTHENTICATION_BACKENDS
				#Efetuando login
				login(request, user)
				request.session['nome'] = user.first_name
				request.session['teste'] = user.id
			#Descobrindo qual o tipo do usuário
			#Isso aqui será alterado
			if tipo.tipo == 'F':
				return  redirect("/Funcionalidades/")
			else:
				return HttpResponse("Você é um provador")
		else:
			return render(request, "Login.html", {"form":form, 'erro':True})
	else:
		return render(request, "Login.html", {"form":form})


def Logout(request):
	try:	
		request.session.clear()
	except KeyError:
		print("Errado")
	return redirect('/')


"""Funções default para o sistema devem ficar nessa página:"""

def edita(request, formulario):
	idTeste = get_test(request)
	#Pegando o usuário 
	usuario = User.objects.get(id = idTeste)	
	if request.method == "POST":
		#Uso o instance para instanciar o objeto para o formulário
		form = formulario(request.POST, instance = usuario)
		if form.is_valid():
			form.save()
			#Falta colocar uma confirmação de "editou!"
			return redirect('/Funcionalidades/')
	else:
		form = formulario(instance=usuario)
	return verificar(request,{'form':form}, 'editar.html')

#Pegando a sessão teste
def get_test(request):
	idTeste = request.session.get('teste')
	return idTeste


#Verificãção de login- toda página criada será preciso chama-la
def  verificar(request, dicionario, html):
	nome = get_name(request)
	dicionario['nome_usuario'] = nome
	if nome is not None:
		return render(request, html, dicionario)
	else:
		return redirect('/')

#Pegando a sessão feita
def get_name(request):
	nome = request.session.get('nome')
	return nome
