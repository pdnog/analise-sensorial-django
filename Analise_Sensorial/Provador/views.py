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

	if controle == 'True':
		respostas = {}

		#RECEBENDO AMOSTRAS, TESTES E PROVADOR PARA CRIAR A NOVA PERGUNTA
		id_amostra = request.GET['amostra']
		provador = get_object_or_404(Provador, id=id_provador)

		#INICIANDO VARIÁVEL
		amostra = None
		hedonica, intencao_compra, dissertativa, boolean = []
		new_respostas = []

		try:
			amostra = Amostra.objects.get(numero=id_amostra, analise_id = id)
			print("That's ok, have one 'amostra' with this pk" )
		except Exception as e:
			#TRATANDO EXCESSÕES NO QUAL O USUÁRIO DIGITE O NÚMERO DE UMA AMOSTRA QUE
			#NÃO HÁ NO BANCO DE DADOS
			print("Do have not any 'amostra' with this pk")

		try:
			teste = Teste.objects.get(id=amostra.teste.id)
			teste.provador = provador
			print("That's ok, have one 'teste' with this pk" )
		except Exception as e:
			print("Do have not any 'teste' with this pk or not have 'amostra' to this 'teste'")

		print(amostra.id)
		for pergunta in perguntas:
			lista_respostas.append(
				(
					str(analise.id),
					str(amostra.id),
					str(teste.id),
					str(pergunta.tipo),
					str(pergunta.id)
				)
			)

		cursor = connection.cursor()
		query = "INSERT INTO fabricante_resposta (analise_id, amostra_id, teste_id, tipo, pergunta_id) VALUES (%s, %s, %s, %s, %s);"
		cursor.executemany(query, new_respostas)

		#SEGUNDA PARTE
		second_query = "SELECT id FROM fabricante_resposta WHERE analise_id = %(analise_id)s AND amostra_id = %(amostra_id)s;"
		dict = {}
		dict['analise_id'] = analise.id
		dict['amostra_id'] = amostra.id
		cursor.execute(second_query, dict)

		#RECEBENDO TODOS OS FORMULÁRIOS
		for index in range(len(perguntas)):
			chave = str(perguntas[index].id)
			if chave in request.GET:
				respostas[chave] = request.GET['' + chave]
				tipo = perguntas[index].tipo
				new_respostas.append((str(analise.id), str(amostra.id), str(teste.id),
				str(tipo), str(perguntas[index].id)))

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
		else:
			intencao_compra.append(object)

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
