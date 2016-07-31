from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import widgets

# Create your models here.
class Analise_Dados_Pessoais(models.Model):
	Nome = models.CharField(max_length=255)
	Descricao = models.TextField()
	Data_Inicio = models.DateTimeField()
	Data_Final = models.DateTimeField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Análise'

class Dados_Numeros_Aleatorios(models.Model):
	QUANT = (
		('2', '2'), 
		('3', '3')
	)
	TAMANHO = (
		('60','60'), 
		('30', '30'), 
		('90', '90'),
		('120', '120'),
		('150', '150'),
		('180', '180'),
		('210', '210'),
		('240', '240'),
		('270', '270'),
		('300', '300')
	)

	quantidade_amostras = models.CharField(max_length=1, choices =QUANT, default='2')
	quantidade_pessoas = models.CharField(max_length=5, choices=TAMANHO, default='180')
	ativado = models.BooleanField()
	analise = models.OneToOneField(Analise_Dados_Pessoais, on_delete=models.CASCADE)

class Numero_Aleatorio(models.Model):
	TIPO = (
		('A','A'), 
		('B','B'), 
		('C','C')
	)
	numero = models.IntegerField()
	analise = models.ForeignKey(Analise_Dados_Pessoais, on_delete=models.CASCADE)
	tipo = models.CharField(max_length=1, choices=TIPO)
	utilizado = models.BooleanField()

