from Fabricante.models import *
from django.shortcuts import redirect, get_object_or_404
from random import randint
from django.db import connection,transaction
from django.core.exceptions import *

#Utilizar o SQL mesmo 
#Gerando 180 testes com 3 amostras em 1:07 min:seg
#Mudar para mysql
#Fazer tudo em uma unica string
#USar fuñções do prórpio banco
#Método antiquado
def gerarando_amostras(id_analise, pessoas, amostras):

	vetor = []
	for i in range(pessoas):
		teste = Teste.objects.create(analise_id=id_analise)

		for j in range(amostras):
			number = randint(100, 999)

			while number in vetor:
				number = randint(100, 999)

			vetor.append(number)

			amostra = Amostra.objects.create(numero=number, tipo=transcricao_numero_letra(j), teste_id=teste.id)


#Utilizando o mysql caiu para 34 segundos 

def gerar_testes(id_analise, pessoas):
	vetor = []
	Testes = []
	cursor = connection.cursor()
	for i in range(pessoas):
		#Criando o array de números
		Testes.append((str(id_analise), None))

	query = 'INSERT INTO Fabricante_teste (analise_id, provador_id) VALUES (%s, %s);'
	#Enviando para o banco de dados
	cursor.executemany(query, Testes)

			


def transcricao_numero_letra(numero):
	VETOR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
	'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

	QUANTIDADE = len(VETOR)

	if numero>QUANTIDADE:
		retorno = numero - QUANTIDADE
		retorno = str(retorno)
		return retorno
	else:
		return VETOR[numero]

#16 segundos com 180 testes

def gerar_amostras(id_analise, amostras):
	#Iniciando um conexão
	cursor = connection.cursor()
		
	vetor_verificar = []
	Amostras = []

	for i in Teste.objects.filter(analise_id=id_analise):

		for j in range(amostras):
			number = randint(100, 999)

			while number in vetor_verificar:
				number = randint(100, 999)

			vetor_verificar.append(number)
			tipo = transcricao_numero_letra(j)
			#Adicionando no vetor
			Amostras.append((str(number), str(tipo), str(i.id), str(id_analise)))

	query = "INSERT INTO Fabricante_amostra (numero, tipo, teste_id, analise_id) VALUES (%s, %s, %s, %s); "
	#Executando a query junto com o vetor
	cursor.executemany(query, Amostras)

def retornar_amostras(id_analise):

	amostras = []
	#Pegando todos as amostras do banco de dados
	for amostra in Amostra.objects.filter(analise_id=id_analise):
		amostras.append(amostra)

	return amostras
	#Precisar fazer uma consulta que pegue todos as análises
	#part_query_one = "SELECT * FROM Fabricante_amostra WHERE teste_id = ();"
	#part_query_two = "SELECT id FROM Fabricante_teste WHERE analise_id = " + str(id_analise)













