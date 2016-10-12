from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from webpage.views import verificar, verificacao_usuario, get_test
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

#USADO PARA SABER QUANTAS PÁGINAS DE FORMULÁRIOS QUE IREMOS CRIAR
contador_amostras = 0

def page_respostas(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	perguntas = Pergunta.objects.filter(analise_id=id)
	id_provador = get_test(request)

	#PRECISA-SE RECEBER O ID DO PROVADOR QUE ESTÁ FAZENDO O TESTE
	#RECENBENDO O CONTROLE DE LAYOUT
	controle = request.GET['controle']
	id_amostra = request.GET['amostra']

	#RECEBENDO AMOSTRAS, TESTES E PROVADOR PARA CRIAR A NOVA PERGUNTA
	amostra = get_object_or_404(Amostra, id_amostra)
	provador = get_object_or_404(Provador, id_provador)
	teste = get_object_or_404(Teste, amostra.teste.id)
	teste.provador = provador

	if controle == 'True':
		respostas = {}

		#RECEBENDO TODOS OS FORMULÁRIOS
		for index in range(len(perguntas)):
			chave = str(perguntas[index].id)
			if chave in request.GET:
				resposta[chave] = request.GET['' + chave]

				#SALVANDO AS PERGUNTAS
				if perguntas[index].tipo == 'PHD':
					#PRECISA-SE CADASTRAR NOVAS PERGUNTAS
					pergunta = PerguntaHedonica.objects.create(analise_id=id,
						pergunta = pergunta[index].pergrunta, hedonica = resposta[chave],
						amostra = amostra, teste = teste)
					#pergunta.hedonica = resposta[chave]
				elif perguntas[index].tipo == 'PSN':
					pergunta = PerguntaSimNao.objects.get(id=perguntas[index].id)
				elif perguntas[index].tipo == 'PDT':
					pergunta = PerguntaDissertativa.objects.get(id=perguntas[index].id)
				else:
					pergunta = PerguntaIntencaoCompra.objects.get(id=perguntas[index].id)

		print (respostas)
		return redirect('/Home_Provador/')

	#QUANDO FOR FALSO ELE IRÁ INICIAR O TESTE SENSORIAL
	else:
		dicionario = formularios(perguntas, id)

	#Tenho que ver como concatenar várias perguntas de tipos diferentes
	return verificar(request, dicionario, 'Provador/responder_analise.html')


""" Lógicas de sistema """
def formularios(perguntas, id):
	#CRIANDO VARIÁVEIS
	hedonica = []
	boolean = []
	intencao_compra = []
	descritiva = []

	for pergunta in perguntas:
		#CRIANDO OBJETOS PARA SEREM RENDERIZADOS PELO TEMPLATE
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

	#ADCIONANDO LISTAS NO DICIONÁRIO
	dicionario = {}
	dicionario['id'] = id
	dicionario['hedonica'] = hedonica
	dicionario['boolean'] = boolean
	dicionario['descritiva'] = descritiva
	dicionario['intencao_compra'] = intencao_compra

	return dicionario

""" Classes de concatenação """
#Classe usada para concatenar a pergunta com o input do formulário
class Word(object):
	"""docstring Word"""
	def __init__(self, pergunta, tipo, id):
		self.pergunta = pergunta
		self.tipo = tipo
		self.id = id
