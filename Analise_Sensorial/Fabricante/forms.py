from django import forms
from Fabricante.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

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
   		self.fields["Data_Final"].required = True

   		#self.fields['Data_Inicio'].widget = widgets.AdminSplitDateTime()
   		#self.fields['Data_Final'].widget = widgets.AdminSplitDateTime()

   		#Colocando textos de ajuda no formulário
   		self.fields["Data_Inicio"].help_text = "Utilize os formatos dd/mm/aaaa e hh:mm"
   		self.fields["Data_Final"].help_text = "Data e hora de término da análise sensorial"

