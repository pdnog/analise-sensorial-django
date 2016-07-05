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

