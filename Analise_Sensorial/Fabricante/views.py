#NEED MORE SPACE
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from Fabricante.forms import *
from Fabricante.models import *
from webpage.forms import *
from webpage.views import edita, get_test, verificar, get_name
from django.contrib.auth.decorators import login_required
from Fabricante.metodos import *

# Create your views here.
def Funcionalidades(request):
	return verificar(request, {}, "Funcoes.html")

def FormDadosAnalise_Page(request):
	form = FormAnaliseSensorial()
	return verificar(request, {'form':form}, "Fabricante/Analise.html")

#Precisa aperfeiçoar esse método
#Quando o usuário cadastrar os números não aparecerá o botão de cadastrar números
def gerar_teste_page(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	if analise.possui_amostras:
		amostras = retornar_amostras(id)
		print(amostras)
		return verificar(request, {'analise':id, 
			'numeros_presentes':analise.possui_amostras, 'amostras':amostras}, 
			"Fabricante/numeros_page.html")
	else:
		return verificar(request, {'analise':id, 
			'numeros_presentes':analise.possui_amostras,}, 
			"Fabricante/numeros_page.html")

def gerar_amostras_action(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	#Métdo antiquado
	#gerando_amostras(id, analise.quantidade_pessoas, analise.quantidade_amostras)
	#Criando analises
	gerar_amostras(id, analise.quantidade_amostras)
	analise.possui_amostras = True
	analise.save()
	return redirect('/MostraAnalise/')

def CadastrarFormAnalise(request):
	if request.method == 'POST':
		form = FormAnaliseSensorial(request.POST)

		if form.is_valid():
			#Campo que diz: Espere, vou adicionar o usuário
			analise = form.save(commit=False)
			#Adicionei o usuário, que é obrigatório
			idTeste = get_test(request)
			usuario = User.objects.get(id = idTeste)	
			analise.user = usuario
			analise.possui_amostras = False
			analise.ativado = False
			#Salvei
			analise.save()
			#Criando testes
			gerar_testes(analise.id, analise.quantidade_pessoas)
			return redirect('/MostraAnalise/')
	else:
		form = FormAnaliseSensorial()
	return verificar(request, {'form':form}, "Fabricante/Analise.html" )

#Edita os dados do fábricante
def editaRed(request):
	return edita(request, FormFabricanteEditar)

#Edita os dados da análise
def editaAnalise(request, id):
	#pegando objeto do banco
	analise = get_object_or_404(AnaliseSensorial, id=id)
	_id_user = get_test(request)
	#comparando o usuario logado com o usuario da analise
	#se o usuário tentar acessar uma anaálise que não é dele,
	# irá ser direcionado a pagina principal
	if analise.user_id == _id_user:
		form = FormAnaliseSensorialEditar(request.POST, instance=analise)
		if form.is_valid() and request.method == 'POST':
			form.save()
			return redirect('/MostraAnalise/')
		else:
			form = FormAnaliseSensorialEditar(instance=analise)
			return verificar(request, {'form':form, 'analise':analise}, 'Fabricante/editarAnalise.html')
	else:
		return redirect('/Funcionalidades/')


#Deletando objeto do banco de dados
def deletar_analise(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	analise.delete()
	return redirect('/MostraAnalise/')

#Retorna as análises cadastradas
def retornaAnalises(request):
	idTeste = get_test(request)
	analise = AnaliseSensorial.objects.filter(user = idTeste)
	if analise is None:
		return HttpResponse("<h1>Nenhuma Análise Cadastrada</h1>")
	else:	
		return verificar(request, {'analise': analise}, 'Fabricante/retornaAnalise.html')

"""Depois arrumamos a repetição de código, 
só estou fazendo isso para mostrar a Jeferson hoje"""
def cadastrarPerguntas(request, id):
	analise = get_object_or_404(AnaliseSensorial, id = id)
	hedonica = True
	if request.method == 'POST':
		#Pegando o request
		form = FormInserirPerguntas(request.POST)
		if form.is_valid():
			#Recebendo o form mas não commitando para o bd
			pergunta = form.save(commit=False)
			#Acrescentadno novos dados de atributos
			pergunta.analise_id = analise.id
			#Inserindo no banco de dados
			pergunta.save()
			return redirect('/MostraAnalise/')
	else:
		form = FormInserirPerguntas()
	return verificar(request,{'form': form, 'analise':analise,'hedonica':hedonica}, 'Fabricante/inserirPergunta.html')

def cadastrarPerguntaDissertativa(request, id):
	analise = get_object_or_404(AnaliseSensorial, id = id)
	dissertativa = True
	if request.method == 'POST':
		#Pegando o request
		form = FormInserirPerguntaDissertativa(request.POST)
		if form.is_valid():
			#Recebendo o form mas não commitando para o bd
			pergunta = form.save(commit=False)
			#Acrescentadno novos dados de atributos
			pergunta.analise_id = analise.id
			#Inserindo no banco de dados
			pergunta.save()
			return redirect('/MostraAnalise/')
	else:
		form = FormInserirPerguntas()
	return verificar(request,{'form': form, 'analise':analise, 'dissertativa':dissertativa}, 'Fabricante/inserirPergunta.html')
	
def cadastrarPerguntaSimNao(request, id):
	analise = get_object_or_404(AnaliseSensorial, id = id)
	simNao = True
	if request.method == 'POST':
		#Pegando o request
		form = FormInserirPerguntaSimNao(request.POST)
		if form.is_valid():
			#Recebendo o form mas não commitando para o bd
			pergunta = form.save(commit=False)
			#Acrescentadno novos dados de atributos
			pergunta.analise_id = analise.id
			#Inserindo no banco de dados
			pergunta.save()
			return redirect('/MostraAnalise/')
	else:
		form = FormInserirPerguntas()
	return verificar(request,{'form': form, 'analise':analise, 'simNao':simNao}, 'Fabricante/inserirPergunta.html')
	
def retornaFormulario (request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	pergunta = Pergunta.objects.filter(analise=analise)
	form = FormMostrarHedonica(request.POST)
	return verificar(request, {'form':form, 'pergunta':pergunta, 'nome':analise.nome}, 'Fabricante/retornaFormulario.html')
	
	
