from django import forms
from webpage.models import *
from django.contrib.auth.forms import UserCreationForm

#Formulário do Fabricante
class FormFabricante(UserCreationForm):
	#Chamando campos do model
	class Meta:
		model = Fabricante
		#username não aceita espaços
		fields = ("first_name", "last_name", "username", "email", "curso")

	def __init__(self, *args, **kwargs):
   		super(FormFabricante, self).__init__(*args, **kwargs)
   		#Adicionando placeholders nos campos
   		self.fields['username'].widget.attrs['placeholder'] = 'Usuário'
   		self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
   		self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
   		self.fields['email'].widget.attrs['placeholder'] = 'Email'
   		self.fields["password1"].widget.attrs["placeholder"] = "Senha"
   		self.fields["password2"].widget.attrs["placeholder"] = "Confirmar senha"

   		#Tornando campos obrigatórios em caso de submissão do formuário
   		self.fields["first_name"].required = True
   		self.fields['email'].required = True

   		#Colocando textos de ajuda no formulário
   		self.fields["curso"].help_text = "Curso que você está matriculado no IFRN."

#Provador formulário
class FormProvador(UserCreationForm):
	"""docstring for FormProvador"""
	class Meta:
		model = Provador
		fields = ("username", "email", "data_nascimento")

	def __init__(self, *args, **kwargs):
		super(FormProvador, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = "Usuário"
		self.fields['email'].widget.attrs['placeholder'] = "Email"
		self.fields['password1'].widget.attrs['placeholder'] = "Senha"
		self.fields['password2'].widget.attrs['placeholder'] = "Confirmar senha"

		#Tornar campos obrigatórios ou retirar
		self.fields['email'].required = True
		