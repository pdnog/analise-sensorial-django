from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from webpage.views import verificar
from Fabricante.models import *
from django.db import connection,transaction
from django.core.exceptions import *
from Fabricante.forms import *

# Create your views here.
""" Renderização de paginas """
def home_provador(request):
	analises = AnaliseSensorial.objects.filter(ativado=True)
	return verificar(request, {"analises":analises}, "Provador/home_provador.html")


def page_respostas(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	perguntas = Pergunta.objects.filter(analise_id=id)
	dicionario = {}

	#Incrementando o dicionário
	dicionario['forms'] = formularios(perguntas, id)
	dicionario['amostras'] = range(analise.quantidade_amostras)
	dicionario['id'] = id

	#Tenho que ver como concatenar várias perguntas de tipos diferentes
	return verificar(request, dicionario, 'Provador/responder_analise.html')


""" Lógicas de sistema """
#Esse método é responsavel por pegar as perguntas e transformas-las em forms
def formularios(perguntas, id):
	#Iniciando variavéis
	objetos = []

	for pergunta in perguntas:
		if pergunta.tipo == 'PSN':
			form = FormPerguntaSimNao(instance=pergunta)
			print(form)
		elif pergunta.tipo == 'PHD':
			form = FormHedonica(instance=pergunta)
		elif pergunta.tipo == 'PDT':
			form = FormDissertativa(instance=pergunta)
		else:
			form = FormIntencaoCompra(instance=pergunta)

		#Iniciando um objeto e atribuindo os atributos 
		object = form_to_renderizar(None, None)
		object.descricao = pergunta.pergunta
		object.formulario = form

		#Adicionando os objetos na lista
		objetos.append(object)

	#Adicionando a lista no dicionário
	return objetos

def receber_formularios(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	if request.method == 'POST':
		print()

	return redirect('/Home_Provador/')

""" Classes de concatenação """
#Classe usada para concatenar a pergunta com o input do formulário 
class form_to_renderizar(object):
	"""docstring for form_to_renderizar"""
	def __init__(self, descricao, formulario):
		self.descricao = descricao
		self.formulario = formulario

		