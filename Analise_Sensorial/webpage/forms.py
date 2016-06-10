from django import forms
from webpage.models import *
from django.contrib.auth.forms import UserCreationForm

#Formulário não utilizado
class FormFabricante(forms.Form):
	username = forms.CharField(label="Nome", max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'Nome'}))
	email = forms.EmailField(label="Email", max_length=75, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	senha = forms.CharField(label="Senha",  max_length=50,widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
	
	TYPE_GROUPS = (
		(u"A", u"Alimentos"),
		(u"B", u"Apicultura"),
	)
	curso = forms.ChoiceField(choices = TYPE_GROUPS)


class FormFabricante2(UserCreationForm):
	#Chamando campos do model
	class Meta:
		model = Fabricante
		#username não aceita espaços
		fields = ("first_name", "last_name","username", "email", "curso")


	#Colocando placeholder nos campos do formulário
	#Colocar todos os campos em placeholder
	def __init__(self, *args, **kwargs):
   		super(FormFabricante2, self).__init__(*args, **kwargs)
   		self.fields['username'].widget.attrs['placeholder'] = 'Usuário'
   		self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
   		self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
   		self.fields['email'].widget.attrs['placeholder'] = 'Email'
   		
