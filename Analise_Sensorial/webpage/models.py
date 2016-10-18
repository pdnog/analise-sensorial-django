from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#Tentar colocar outro tipo de usuário
class Fabricante(User):
	TYPE_GROUPS = (
		(u"A", u"Alimentos"),
		(u"B", u"Apicultura"),
	)
	#Apresenta no admin o que foi povoado em TYPE_PRODUTS
	#Defini o padrão (A)
	#Choice pode ser usado para radiobutton, checkbox e selection
	curso = models.CharField(max_length = 1, choices = TYPE_GROUPS, default = u"A")
	YEAR = (
		(u"1", "1º Ano"),
		(u"2", "2º Ano"),
		(u"3", "3º Ano"),
		(u"4", "4º Ano")
	)
	ano = models.CharField(max_length = 1, choices = YEAR, default = u"1")

	#Criando uma chave estrangeira para User, depois analisar com o SQLite3
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = "Fabricante"


class Provador(User):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	data_nascimento = models.DateField("Data de Nascimento")
	sexoChoices = (
		(u"1", "Masculino"),
		(u"2", "Feminino"),
	)
	sexo = models.CharField(max_length = 1, choices = sexoChoices, default = u"1")
	class Meta:
		verbose_name = "Provador"
		verbose_name_plural = "Provadores"


class Tipagem(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	TYPE_USER = (
		(u'F', u'Fabricante'), 
		(u'P', u'Provador')
	)
	tipo = models.CharField(max_length=1, choices=TYPE_USER) 
