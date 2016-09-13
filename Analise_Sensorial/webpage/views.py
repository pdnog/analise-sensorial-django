from django.shortcuts import render, redirect, get_object_or_404
from webpage.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from webpage.models import *
from webpage.utilitarios import confirmacao_cadastro
from django.http import HttpResponse
from django.template.context_processors import request


# Create your views here.
#Jogando o formulário para o html

#Iniciando a classe
_confirmacao = confirmacao_cadastro()

def render_com_login(request, html, dicionario):
	dicionario['form_login'] = FormLogin()
	return render(request, html, dicionario)


def Inicio(request):
	return render_com_login(request, "home.html", {})

def Fabricante_page_cadastro(request):
	form = FormFabricante()
	return render_com_login(request, "Fabricante.html", {"form":form})

def Provador_page_cadastro(request):
	form = FormProvador()
	return render_com_login(request, "Provador.html", {"form":form})

def Cadastro_principal_page(request):
	return render_com_login(request, "cadastro_principal.html", {})
#Cadastro default
def Cadastro_User(request, formulario, html, tipoUser):
	if request.method == 'POST':
		form = formulario(request.POST)
		#Vendo se o formário com o resquest é válido, se for, ele salva no models, pois o form é uma extensão do model
		if form.is_valid():
			form.save()
			#Retornando o usuário do formulario
			username = form.cleaned_data['username']
			#Retornando o objeto usuário
			usuario = User.objects.get(username=username)
			#Definindo o tipo de usuário pelo ID
			tipagem = Tipagem.objects.create(user_id=usuario.id, tipo=tipoUser)
			#Setando "True" ao parametro da classe
			_confirmacao.setConfirmacao(True)
			#Redirecionando para a página principal
			return redirect("/")
	else:
		#Se o método não for POST, ele mostra um formulário em branco
		form = formulario()
	return render_com_login(request, html, {"form":form})


#Cadastrando um fabricante
def Cadastro_Fabricante(request):
	return Cadastro_User(request, FormFabricante, "fabricante.html", 'F')
	
#Cadastrando um provador
def Cadastro_Provador(request):
	return Cadastro_User(request, FormProvador,"Provador.html",'P')
	
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

	return render_com_login(request, "Login.html", {"form":form, "confirmacao":confirm})

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
				request.session['id'] = user.id
			#Descobrindo qual o tipo do usuário
			#Isso aqui será alterado
			if tipo.tipo == 'F':
				return  redirect("/MostraAnalise/")
			else:
				#Redirecionar provador para outra página
				return redirect("/Home_Provador/")
		else:
			return render_com_login(request, "Login.html", {"form":form, 'erro':True})
	else:
		return render_com_login(request, "Login.html", {"form":form})


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
	tipagem = Tipagem.objects.get(pk = idTeste)	
	if request.method == "POST":
		#Uso o instance para instanciar o objeto para o formulário
		form = formulario(request.POST, instance = usuario)
		if form.is_valid():
			form.save()
			#Falta colocar uma confirmação de "editou!"
			return redirect('/Funcionalidades/')
	else:
		form = formulario(instance=usuario)
	if tipagem.tipo == "F":
		return verificarFabricante(request,{'form':form}, 'editar.html')
	else:
		return verificarProvador(request,{'form':form}, 'editar.html',)

#Pegando a sessão teste
def get_test(request):
	idTeste = request.session.get('id')
	return idTeste




#Verificãção de login- toda página criada será preciso chama-la

def verificarFabricante(request, dicionario, html):
	id = get_test(request)
	tipoUsuario = Tipagem.objects.get(pk = id)
	if tipoUsuario.tipo == "P":
		redirect("/MostraAnalises/")
	else:
		nome = get_name(request)
		dicionario['nome_usuario'] = nome
		if nome is not None:
			return render(request, html, dicionario) 
		else:
			return redirect('/')	
	
def verificarProvador(request, dicionario, html):
	id = get_test(request)
	tipoUsuario = Tipagem.objects.get(pk = id)
	if tipoUsuario.tipo == "F":
		redirect("/Logout/")
	else:
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

#Quando o usuário digirar uma url que não pertença a ele, ele será deslogado e irá para tela inicial
def verificacao_usuario(request, analise):
	if(analise.user.first_name != get_name(request)):
		return Logout(request)
