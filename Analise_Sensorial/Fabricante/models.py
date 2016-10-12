from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from webpage.models import Provador

# Create your models here.
class AnaliseSensorial(models.Model):
	nome = models.CharField(max_length=255)
	descricao = models.TextField()
	data_Inicio = models.DateField()
	time_Inicio = models.TimeField()
	time_Final = models.TimeField()
	data_Final = models.DateField()
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
	teste = models.ForeignKey(Teste, on_delete=models.CASCADE, null=True)
	amostra = models.ForeignKey(Amostra, on_delete=models.CASCADE, null=True)
	pergunta = models.TextField()
	default = models.BooleanField(default=False)

	TYPE = (
		('PSN', 'Pergunta sim/não'),
		('PHD', 'Pergunta hedônica'),
		('PDT', 'Pergunta dissertativa'),
		('PIC', 'Pergunta de inteção de compra'),
		)

	tipo = models.CharField(choices=TYPE, max_length=4)

	class Meta:
		verbose_name = 'Pergunta'
		verbose_name_plural = 'Perguntas'

	def __str__(self):
		return self.pergunta

class PerguntaSimNao(Pergunta):
	resposta = models.BooleanField(default=False)


class PerguntaHedonica(Pergunta):
	escala = ((1, 'Desgostei extremamente (detestei)'),
		(2, 'Desgostei muito'),
		(3, 'Desgostei moderadamente'),
		(4, 'Desgostei ligeiramente'),
		(5, 'Nem gostei / Nem desgostei'),
		(6, 'Gostei ligeiramente'),
		(7, 'Gostei moderadamente'),
		(8, 'Gostei muito'),
		(9, 'Gostei muitíssimo (adorei)'),
		)
	hedonica = models.IntegerField(choices=escala, null=True)

class PerguntaDissertativa(Pergunta):
	descricao = models.TextField()


class PerguntaIntencaoCompra(Pergunta):
	LEVEL = (
		(1, 'Certamente não compraria o produto'),
		(2, 'Possivelmente não compraria o produto'),
		(3, 'Talvez comprasse / Talvez não comprasse'),
		(4, 'Possivelmente compraria o produto'),
		(5, 'Certamente compraria o produto')
		)

	compra = models.IntegerField(choices=LEVEL, null=True)
