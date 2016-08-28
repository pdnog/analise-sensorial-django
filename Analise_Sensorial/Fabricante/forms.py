from django import forms
from Fabricante.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from functools import partial

class FormAnaliseSensorial(forms.ModelForm):
	class Meta:
		model = AnaliseSensorial
		fields = ("nome","data_Inicio", "data_Final", "quantidade_pessoas", "quantidade_amostras", "descricao")

	def __init__(self, *args, **kwargs):
	   	super(FormAnaliseSensorial, self).__init__(*args, **kwargs)
	   	#Adicionando placeholders nos campos
	   	self.fields['nome'].widget.attrs['placeholder'] = 'Nome'
	   	self.fields['descricao'].widget.attrs['placeholder'] = 'Descrição'
	   	self.fields['data_Inicio'].widget.attrs['placeholder'] = 'Data e hora inicial'
	   	self.fields['data_Final'].widget.attrs['placeholder'] = 'Data e hora final'
	   	self.fields['quantidade_pessoas'].widget.attrs['placeholder'] = 'Quantidade de pessoas'
	   	self.fields['quantidade_amostras'].widget.attrs['placeholder'] = 'Quantidade de amostras'

	   	#Colocando as labels no campo
	   	self.fields['descricao'].label = "Descrição"
	   	self.fields['data_Inicio'].label = "Início"
	   	self.fields['data_Final'].label = "Término"
	   	self.fields['quantidade_pessoas'].label = 'Quantidade de pessoas'
	   	self.fields['quantidade_amostras'].label = 'Quantidade de amostras'
	   	
	   	#Tornando campos obrigatórios em caso de submissão do formuário
	   	self.fields["nome"].required = True
	   	self.fields['descricao'].required = False
	   	self.fields["data_Inicio"].required = True
	   	self.fields["data_Final"].required = False
	   	self.fields['quantidade_pessoas'].required = True
	   	self.fields['quantidade_amostras'].required = True

	   	#self.fields['Data_Inicio'].widget = widgets.AdminSplitDateTime()
	   	#self.fields['Data_Final'].widget = widgets.AdminSplitDateTime()

	   	#Colocando textos de ajuda no formulário
	   	self.fields["data_Inicio"].help_text = "Utilize os formatos dd/mm/aaaa e hh:mm"
	   	self.fields["data_Final"].help_text = "Data e hora de término da análise sensorial"
	   	self.fields['quantidade_pessoas'].help_text = 'Quantidade de pessoas para o teste sensorial'
	   	self.fields['quantidade_amostras'].help_text = 'Quantidade de amostras que você terá em sua análise, aconselhamos que esse campo seja menor que 23'

class FormAnaliseSensorialEditar(forms.ModelForm):
	   """docstring for FormAnaliseSensorialEditar"""
	   class Meta:
	   	model = AnaliseSensorial
	   	fields = ('nome', 'data_Inicio', 'data_Final', 'descricao')
	   def __init__(self, *args, **kwargs):
	   	super(FormAnaliseSensorialEditar, self).__init__(*args, **kwargs)
	   	#Adicionando placeholders nos campos
	   	self.fields['nome'].widget.attrs['placeholder'] = 'Nome'
	   	self.fields['descricao'].widget.attrs['placeholder'] = 'Descrição'
	   	self.fields['data_Inicio'].widget.attrs['placeholder'] = 'Data e hora inicial'
	   	self.fields['data_Final'].widget.attrs['placeholder'] = 'Data e hora final'

	   	#Colocando as labels no campo
	   	self.fields['descricao'].label = "Descrição"
	   	self.fields['data_Inicio'].label = "Início"
	   	self.fields['data_Final'].label = "Término"
	   	
	   	#Tornando campos obrigatórios em caso de submissão do formuário
	   	self.fields["nome"].required = True
	   	self.fields['descricao'].required = False
	   	self.fields["data_Inicio"].required = True
	   	self.fields["data_Final"].required = False

	   	#self.fields['Data_Inicio'].widget = widgets.AdminSplitDateTime()
	   	#self.fields['Data_Final'].widget = widgets.AdminSplitDateTime()

	   	#Colocando textos de ajuda no formulário
	   	self.fields["data_Inicio"].help_text = "Utilize os formatos dd/mm/aaaa e hh:mm"
	   	self.fields["data_Final"].help_text = "Data e hora de término da análise sensorial"
         

class FormInserirPerguntas(forms.ModelForm):
	class Meta:
		model = PerguntaHedonica
		fields = ('pergunta','analise')
