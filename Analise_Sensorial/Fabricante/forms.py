from django import forms
from Fabricante.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from functools import partial

class FormDadosAnalise(forms.ModelForm):
	class Meta:
		model = Analise_Dados_Pessoais
		fields = ("Nome","Data_Inicio", "Data_Final", "Descricao")

	def __init__(self, *args, **kwargs):
   		super(FormDadosAnalise, self).__init__(*args, **kwargs)
   		#Adicionando placeholders nos campos
   		self.fields['Nome'].widget.attrs['placeholder'] = 'Nome'
   		self.fields['Descricao'].widget.attrs['placeholder'] = 'Descrição'
   		self.fields['Data_Inicio'].widget.attrs['placeholder'] = 'Data e hora inicial'
   		self.fields['Data_Final'].widget.attrs['placeholder'] = 'Data e hora final'
   		#Colocando as labels no campo
   		self.fields['Descricao'].label = "Descrição"
   		self.fields['Data_Inicio'].label = "Início"
   		self.fields['Data_Final'].label = "Término"
   		#Tornando campos obrigatórios em caso de submissão do formuário
   		self.fields["Nome"].required = True
   		self.fields['Descricao'].required = True
   		self.fields["Data_Inicio"].required = True
   		self.fields["Data_Final"].required = False

   		#self.fields['Data_Inicio'].widget = widgets.AdminSplitDateTime()
   		#self.fields['Data_Final'].widget = widgets.AdminSplitDateTime()

   		#Colocando textos de ajuda no formulário
   		self.fields["Data_Inicio"].help_text = "Utilize os formatos dd/mm/aaaa e hh:mm"
   		self.fields["Data_Final"].help_text = "Data e hora de término da análise sensorial"

class FormDadosNumerosAleatorios(forms.ModelForm):
   """docstring for FormDadosNumerosAleatorios"""
   class Meta:
      model = Dados_Numeros_Aleatorios
      fields = ('quantidade_amostras', 'quantidade_pessoas',)
   def __init__(self, *args, **kwargs):
      super(FormDadosNumerosAleatorios, self).__init__(*args, **kwargs)
      self.fields['quantidade_amostras'].label = 'Amostras'
      self.fields['quantidade_amostras'].help_text = 'Quantidade de tipo de amostra'
      self.fields['quantidade_amostras'].required = True
      self.fields['quantidade_pessoas'].label = 'Pessoas'
      self.fields['quantidade_pessoas'].help_text = 'Quantidade de pessoas que participarão da análise sensorial'
      self.fields['quantidade_pessoas'].required = True
      
         

