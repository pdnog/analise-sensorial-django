from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from webpage.models import Provador

# Create your models here.
class AnaliseSensorial(models.Model):
	nome = models.CharField(max_length=255)
	descricao = models.TextField()
	data_Inicio = models.DateTimeField()
	data_Final = models.DateTimeField()
	possui_amostras = models.BooleanField()
	ativado = models.BooleanField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quantidade_amostras = models.IntegerField()
	quantidade_pessoas = models.IntegerField()

	def __str__ (self):
		return self.nome

	class Meta:
		verbose_name = 'Análise'


class Teste(models.Model):
	#Esse campo será incrementado mais para frente
	analise = models.ForeignKey(AnaliseSensorial, on_delete=models.CASCADE)
	provador = models.OneToOneField(Provador, on_delete=models.CASCADE, null=True)

	class Meta:
		verbose_name = 'Teste sensorial'
		verbose_name_plural = 'Testes sensoriais'

	def __str__(self):
		_numero = str(self.id)
		return _numero

class Amostra(models.Model):
	teste = models.ForeignKey(Teste, on_delete=models.CASCADE)
	numero = models.IntegerField()
	tipo = models.CharField(max_length=10)
	analise = models.ForeignKey(AnaliseSensorial, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Amostra'
		verbose_name_plural = 'Amostras'

	def __str__(self):
		_numero = str(self.numero)
		return _numero

class Pergunta(models.Model):
	analise = models.ForeignKey(AnaliseSensorial, on_delete=models.CASCADE)
	pergunta = models.CharField(max_length=255)

class PerguntaSimNao(Pergunta):
	nao = models.BooleanField(default=False, verbose_name='Não')
	sim = models.BooleanField(default=False, verbose_name='Sim')


class PerguntaHedonica(Pergunta):
	escala = ((1, 'Desgostei Muitissimo'),
		(2, 'Desgostei Moderadamente'),
		(3, 'Gostei'), 
		(4, 'Gostei Moderadamente'),
		(5, 'Gostei Muitissimo'))
	hedonica = models.IntegerField(choices=escala, null=True, blank = True)

class PerguntaDissertativa(Pergunta):
	descricao = models.TextField()
