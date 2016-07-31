#Geradores de números aleatórios seraão implementados aqui
from random import randint

vetor_verificacao = []

def popular_vetor(pessoas):
	vetor = []

	for x in range(pessoas):
		numero = randint(100, 999)

		while numero in vetor_verificacao[]:
			numero = randint(100, 999)

		vetor.append(numero)
		vetor_verificacao.append(numero)

	return vetor


