from Fabricante.models import *
from django.shortcuts import redirect, get_object_or_404
from random import randint

#Utilizar o SQL mesmo 
#Gerando 180 testes com 3 amostras em 1:07 min:seg
#Mudar para mysql
#Fazer tudo em uma unica string
#USar fuñções do prórpio banco
def gerar_amostras(id_analise, pessoas, amostras):
	vetor = []
	for i in range(pessoas):
		teste = Teste.objects.create(analise_id=id_analise)

		for j in range(amostras):
			number = randint(100, 999)

			while number in vetor:
				number = randint(100, 999)

			vetor.append(number)

			amostra = Amostra.objects.create(numero=number, tipo=transcricao_numero_letra(j), teste_id=teste.id)


def gerar_amostra(id_analise, pessoas, amostras):
	vetor = []
	for i in range(pessoas):
		teste = Teste.objects.create(analise_id=id_analise)

		for j in range(amostras):
			number = randint(100, 999)

			while number in vetor:
				number = randint(100, 999)

			vetor.append(number)

			amostra = Amostra.objects.create(numero=number, tipo=transcricao_numero_letra(j), teste_id=teste.id)


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
def gerando_testes(id_analise, pessoas):
	for i in range(pessoas):
		teste= Teste.objects.create(analise_id=id_analise)

def gerando_amostras(id_analise, amostras):
	try:
		vetor = Teste.objects.filter(analise_id=id_analise)
	except Teste.DoesNotExist:
		print('Erro')
		
	vetor_verificar = []

	for i in vetor:
		for j in range(amostras):
			number = randint(100, 999)

			while number in vetor:
				number = randint(100, 999)

			vetor_verificar.append(number)
			amostra = Amostra.objects.create(numero=number, tipo=transcricao_numero_letra(j), teste_id=vetor[i].id)












