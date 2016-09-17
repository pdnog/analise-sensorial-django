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

	dicionario = many_asks(perguntas)
	dicionario['forms'] = formularios(perguntas, id)
	dicionario['amostras'] = range(analise.quantidade_amostras)
	dicionario['id'] = id

	#Tenho que ver como concatenar várias perguntas de tipos diferentes
	return verificar(request, dicionario, 'Provador/responder_analise.html')


""" Lógicas de sistema """

""" Esse método é responsavel por pegar as perguntas e transformas-las em forms, utilizado
anteriormente """

def formularios(perguntas, id):
	#Iniciando variavéis
	objetos = []

	for pergunta in perguntas:
		if pergunta.tipo == 'PSN':
			form = FormPerguntaSimNao(instance=pergunta)
		elif pergunta.tipo == 'PHD':
			form = FormHedonica(instance=pergunta)
		elif pergunta.tipo == 'PDT':
			form = FormDissertativa(instance=pergunta)
		else:
			form = FormIntencaoCompra(instance=pergunta)

		#print(form)
		#Iniciando um objeto e atribuindo os atributos 
		object = form_to_renderizar(None, None)
		object.descricao = pergunta.pergunta
		object.formulario = form

		#Adicionando os objetos na lista
		objetos.append(object)

	#Adicionando a lista no dicionário
	return objetos

#Esse daqui é voltado para o formset, e repetição de forms do mesmo tipo 
def formsets(perguntas):
	GeneralFormset = formset_factory(General, extra=len(perguntas))
	#kwargs = [{'tipo':x.tipo, 'ask':x.pergunta} for x in perguntas]
	#GeneralFormset.form = staticmethod(curry(General, *kwargs))
	"""for pergunta in perguntas:
		kwargs = {'tipo':pergunta.tipo, 'ask':pergunta.pergunta}
		GeneralFormset.form = staticmethod(curry(General, **kwargs))
		print(pergunta.pergunta)"""	

	"""args = []
	for pergunta in perguntas:
		kwargs = {'tipo':pergunta.tipo, 'ask':pergunta.pergunta}
		args.append(kwargs)"""

	formset = GeneralFormset(initial=[])

	for index in range(len(perguntas)):
		formset[index].titulo = perguntas[index].pergunta
		formset[index].tipo = perguntas[index].tipo
		formset[index].__init__

	for form in formset:
		print(form)

	return formset

#Podemos utilizar o JS para fazer a repetição de inputs e ver algum jeito de pegar todos
def many_asks(perguntas):
	yes_or_no = []
	hedonic_scale = []
	essay = []
	buy_intention = []

	for pergunta in perguntas:

		if pergunta.tipo == 'PSN':
			yes_or_no.append(pergunta)

		elif pergunta.tipo == 'PHD':
			hedonic_scale.append(pergunta)

		elif pergunta.tipo == 'PDT':
			essay.append(pergunta)

		else:
			buy_intention(pergunta)

	dictionary = {}
	dictionary['yes_or_no'] = yes_or_no
	dictionary['hedonic_scale'] = hedonic_scale
	dictionary['essay'] = essay
	dictionary['buy_intention'] = buy_intention

	dictionary['size_yes_or_no'] = len(yes_or_no)
	dictionary['size_hedonic_scale'] = len(hedonic_scale)
	dictionary['size_essay'] = len(essay)
	dictionary['size_buy_intention'] = len(buy_intention)

	return dictionary


def receber_formularios(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)

	if request.method == 'POST':
		pass

	return redirect('/Home_Provador/')


""" Classes de concatenação """
#Classe usada para concatenar a pergunta com o input do formulário 
class form_to_renderizar(object):
	"""docstring for form_to_renderizar"""
	def __init__(self, descricao, formulario):
		self.descricao = descricao
		self.formulario = formulario
