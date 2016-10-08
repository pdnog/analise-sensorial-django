from django import forms
from Fabricante.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from functools import partial

class FormAnaliseSensorial(forms.ModelForm):
	class Meta:
		model = AnaliseSensorial
		fields = ("nome","data_Inicio","time_Inicio" ,"data_Final", "time_Final", "quantidade_pessoas", "quantidade_amostras", "descricao")

	def __init__(self, *args, **kwargs):
	   	super(FormAnaliseSensorial, self).__init__(*args, **kwargs)
	   	#Adicionando placeholders nos campos
	   	self.fields['nome'].widget.attrs['placeholder'] = 'Nome'
	   	self.fields['descricao'].widget.attrs['placeholder'] = 'Descrição'
	   	self.fields['data_Inicio'].widget.attrs['placeholder'] = 'Data inicial'
	   	self.fields['data_Final'].widget.attrs['placeholder'] = 'Data final'
	   	self.fields['quantidade_pessoas'].widget.attrs['placeholder'] = 'Quantidade de pessoas'
	   	self.fields['quantidade_amostras'].widget.attrs['placeholder'] = 'Quantidade de amostras'

	   	#Colocando as labels no campo
	   	self.fields['descricao'].label = "Descrição:"
	   	self.fields['data_Inicio'].label = "Data inicial:"
	   	self.fields['data_Final'].label = "Data final:"
	   	self.fields['nome'].label = "Nome:"
	   	self.fields['time_Inicio'].label = "Hora inicial:"
	   	self.fields['time_Final'].label = "Hora final:"
	   	self.fields['quantidade_pessoas'].label = 'Quantidade de pessoas:'
	   	self.fields['quantidade_amostras'].label = 'Quantidade de amostras:'

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
	   	self.fields["data_Inicio"].help_text = "Data do inicio da análise sensorial"
	   	self.fields["data_Final"].help_text = "Data de término da análise sensorial"
	   	self.fields['time_Inicio'].help_text = "Hora de inicio da análise sensorial"
	   	self.fields['time_Final'].help_text = "Hora de término da análise sensorial"
	   	self.fields['quantidade_pessoas'].help_text = 'Quantidade de pessoas para o teste sensorial'
	   	self.fields['quantidade_amostras'].help_text = 'Quantidade de amostras que você terá em sua análise, aconselhamos que esse campo seja menor que 23'

class FormAnaliseSensorialEditar(forms.ModelForm):
	   """docstring for FormAnaliseSensorialEditar"""
	   class Meta:
	   	model = AnaliseSensorial
	   	fields = ('nome', 'data_Inicio', 'time_Inicio', 'time_Final','data_Final', 'descricao')
	   def __init__(self, *args, **kwargs):
	   	super(FormAnaliseSensorialEditar, self).__init__(*args, **kwargs)
	   	#Adicionando placeholders nos campos
	   	self.fields['nome'].widget.attrs['placeholder'] = 'Nome'
	   	self.fields['descricao'].widget.attrs['placeholder'] = 'Descrição'
	   	self.fields['data_Inicio'].widget.attrs['placeholder'] = 'Data e hora inicial'
	   	self.fields['data_Final'].widget.attrs['placeholder'] = 'Data e hora final'

	   	#Colocando as labels no campo
	   	self.fields['descricao'].label = "Descrição:"
	   	self.fields['data_Inicio'].label = "Data inicial:"
	   	self.fields['data_Final'].label = "Data final:"
	   	self.fields['nome'].label = "Nome:"
	   	self.fields['time_Inicio'].label = "Hora inicial:"
	   	self.fields['time_Final'].label = "Hora final:"

	   	#Tornando campos obrigatórios em caso de submissão do formuário
	   	self.fields["nome"].required = True
	   	self.fields['descricao'].required = False
	   	self.fields["data_Inicio"].required = True
	   	self.fields["data_Final"].required = False
	   	self.fields["descricao"].widget.attrs['rows'] = 5

	   	#self.fields['Data_Inicio'].widget = widgets.AdminSplitDateTime()
	   	#self.fields['Data_Final'].widget = widgets.AdminSplitDateTime()

	   	#Colocando textos de ajuda no formulário
	   	self.fields["data_Inicio"].help_text = "Data do inicio da análise sensorial"
	   	self.fields["data_Final"].help_text = "Data de término da análise sensorial"
	   	self.fields['time_Inicio'].help_text = "Hora de inicio da análise sensorial"
	   	self.fields['time_Final'].help_text = "Hora de término da análise sensorial"

#Não necessita usar analise aqui, pois quando ele clicar em perguntas,
#já irá pegar o id da análise selecionada
class FormInserirPerguntas(forms.ModelForm):
	#pergunta = forms.CharField(widget=forms.Textarea)
	TYPE = (
		('PSN', 'Pergunta sim/não'),
		('PHD', 'Pergunta hedônica'),
		('PDT', 'Pergunta dissertativa'),
		('PIC', 'Pergunta de inteção de compra'),
		)

	tipo = forms.ChoiceField(choices = TYPE)

	class Meta:
		model = Pergunta
		fields = ('pergunta', 'tipo')

	def __init__(self, *args, **kwargs):
		super(FormInserirPerguntas, self).__init__(*args, **kwargs)
		self.fields['tipo'].help_text = 'Esse campo determina qual tipo de pergunta vai aparecer pro usuário'
		self.fields['tipo'].required = True
		self.fields['pergunta'].required = True
		self.fields['pergunta'].widget.attrs['required'] = 'true'
		#self.fields['pergunta'].widget.attrs['oninvalid'] = "this.setCustomValidity(\'Campo requerido\')"
		#Definindo qauntidade de linhas do textfield
		self.fields['pergunta'].widget.attrs['rows'] = 5


class FormDissertativa(forms.ModelForm):
	class Meta:
		model = PerguntaDissertativa
		fields = ('descricao',)

	def __init__(self, *args, **kwargs):
		super(FormDissertativa, self).__init__(*args, **kwargs)
		self.fields['descricao'].widget.attrs['rows'] = 3
		self.fields['descricao'].label = ''
		#self.fields['descricao'].widget.attrs['name'] = str(id)

class FormPerguntaSimNao(forms.ModelForm):
	YESNO_CHOICES = ((True, 'Não'), (False, 'Sim'))
	resposta = forms.TypedChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect)

	class Meta:
		model = PerguntaSimNao
		fields = ('resposta',)

	def __init__(self, *args, **kwargs):
		super(FormPerguntaSimNao, self).__init__(*args, **kwargs)
		self.fields['resposta'].label = ''

class FormHedonica(forms.ModelForm):
	class Meta:
		model = PerguntaHedonica
		fields = ('hedonica',)

	def __init__(self, *args, **kwargs):
		super(FormHedonica, self).__init__(*args, **kwargs)
		self.fields['hedonica'].label = ''

class FormIntencaoCompra(forms.ModelForm):
	class Meta:
		model = PerguntaIntencaoCompra
		fields = ('compra',)

	def __init__(self, *args, **kwargs):
		super(FormIntencaoCompra, self).__init__(*args, **kwargs)
		self.fields['compra'].label = ''


class General(forms.Form):
	#Campo para a pergunta de sim ou não
	YESNO_CHOICES = ((True, 'Não'), (False, 'Sim'))
	yes_or_no = forms.TypedChoiceField(choices=YESNO_CHOICES,
		widget=forms.RadioSelect, disabled=True, label='')

	#Campo para a pergunta hedônica
	SCALE_CHOICES = ((1, 'Desgostei extremamente (detestei)'),
		(2, 'Desgostei muito'),
		(3, 'Desgostei moderadamente'),
		(4, 'Desgostei ligeiramente'),
		(5, 'Nem gostei / Nem desgostei'),
		(6, 'Gostei ligeiramente'),
		(7, 'Gostei moderadamente'),
		(8, 'Gostei muito'),
		(9, 'Gostei muitíssimo (adorei)'),
		)

	hedonic_scale = forms.TypedChoiceField(choices=SCALE_CHOICES, disabled=True, label='')

	#Campo para a pergunta dissertativa
	essay = forms.CharField(widget=forms.Textarea(attrs={'size':3}),
		disabled=True, label='')


	#Campo para a pergunta de intenção de compra
	BUY_CHOICES = (
			(1, 'Certamente não compraria o produto'),
			(2, 'Possivelmente não compraria o produto'),
			(3, 'Talvez comprasse / Talvez não comprasse'),
			(4, 'Possivelmente compraria o produto'),
			(5, 'Certamente compraria o produto')
			)

	buy_intention = forms.TypedChoiceField(choices=BUY_CHOICES, disabled=True, label='')

	def __init__(self, *args, **kwargs):
		super(General, self).__init__(*args, **kwargs)
		self.tipo = None
		self.tipo = None

		#Campos e condições de enable ou disable
		if(self.tipo=='PSN'):
			self.fields['buy_intention'].help_text = 'Eu sou limão'
			fields=('yes_or_no')

		elif(self.tipo=='PHD'):
			fields = ('hedonic_scale',)

		elif(self.tipo=='PDT'):
			fields = ('essay',)

		elif(self.tipo=='PIC'):
			fields = ('buy_intention',)
