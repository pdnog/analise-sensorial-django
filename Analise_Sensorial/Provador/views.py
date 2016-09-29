from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from webpage.views import verificar
from django.forms import formset_factory, BaseFormSet
from django.utils.functional import curry
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

	"""if request.method == 'GET':
		respostas = []

		for index in range(len(perguntas)):
			if str(perguntas[index].id) in request.GET:
				respostas[index] = request.GET['' + str(perguntas[index].id)]

		print(respostas)

		return redirect('/Home_Provador/')"""

	if True==False:
		pass
	else:
		dicionario = many_asks(perguntas)
		dicionario['amostras'] = range(analise.quantidade_amostras)
		dicionario['id'] = id


	#Tenho que ver como concatenar várias perguntas de tipos diferentes
	return verificar(request, dicionario, 'Provador/responder_analise.html')


""" Lógicas de sistema """
def many_asks(perguntas):
	hedonica = []
	boolean = []
	intencao_compra = []
	descritiva = []

	for pergunta in perguntas:
		object = Word(None, None, None)
		object.pergunta = pergunta.pergunta
		object.id = pergunta.id
		object.tipo = pergunta.tipo

		if pergunta.tipo == 'PHD':
			hedonica.append(object)
		elif pergunta.tipo == 'PSN':
			boolean.append(object)
		elif pergunta.tipo == 'PDT':
			descritiva.append(object)
		elif pergunta.tipo == 'PIC':
			intencao_compra.append(object)
		else:
			pass

	dicionario = {}
	dicionario['hedonica'] = hedonica
	dicionario['boolean'] = boolean
	dicionario['descritiva'] = descritiva
	dicionario['intencao_compra'] = intencao_compra

	return dicionario

def receber_formularios(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	perguntas = Pergunta.objects.filter(analise_id=id)

	if request.method == 'GET':
		respostas = []

		for index in range(len(perguntas)):
			if str(perguntas[index].id) in request.GET:
				respostas.append(request.GET['' + str(perguntas[index].id)])

		print(respostas)

		return redirect('/Home_Provador/')

	return redirect('/Home_Provador/')


""" Classes de concatenação """
#Classe usada para concatenar a pergunta com o input do formulário
class Word(object):
	"""docstring Word"""
	def __init__(self, pergunta, tipo, id):
		self.pergunta = pergunta
		self.tipo = tipo
		self.id = id
