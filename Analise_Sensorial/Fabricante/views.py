#NEED MORE SPACE
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from Fabricante.forms import *
from Fabricante.models import *
from webpage.forms import *
from webpage.views import edita, get_test, verificar, get_name, Logout
from django.contrib.auth.decorators import login_required
from Fabricante.metodos import *

#Quando o usuário digirar uma url que não pertença a ele, ele será deslogado e irá para tela inicial
def verificacao_usuario(request, analise):
	if(analise.user.first_name != get_name(request)):
		return Logout(request)


# Create your views here.
def Funcionalidades(request):
	return verificar(request, {}, "Funcoes.html")

def FormDadosAnalise_Page(request):
	form = FormAnaliseSensorial()
	return verificar(request, {'form':form}, "Fabricante/Analise.html")

#Precisa aperfeiçoar esse método
#Quando o usuário cadastrar os números não aparecerá o botão de cadastrar números
def gerar_teste_page(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	verificacao_usuario(request, analise)
	if analise.possui_amostras:
		amostras = retornar_amostras(id)
		print(amostras)
		return verificar(request, {'analise':id, 
			'numeros_presentes':analise.possui_amostras, 'amostras':amostras}, 
			"Fabricante/numeros_page.html")
	else:
		return verificar(request, {'analise':id, 
			'numeros_presentes':analise.possui_amostras,}, 
			"Fabricante/numeros_page.html")

def gerar_amostras_action(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	verificacao_usuario(request, analise)
	#Métdo antiquado
	#gerando_amostras(id, analise.quantidade_pessoas, analise.quantidade_amostras)
	#Criando analises
	gerar_amostras(id, analise.quantidade_amostras)
	analise.possui_amostras = True
	analise.save()
	return redirect('/MostraAnalise/')

def CadastrarFormAnalise(request):
	if request.method == 'POST':
		form = FormAnaliseSensorial(request.POST)

		if form.is_valid():
			#Campo que diz: Espere, vou adicionar o usuário
			analise = form.save(commit=False)
			#Adicionei o usuário, que é obrigatório
			idTeste = get_test(request)
			usuario = User.objects.get(id = idTeste)	
			analise.user = usuario
			analise.possui_amostras = False
			analise.ativado = False
			#Salvei
			analise.save()
			#Criando testes
			gerar_testes(analise.id, analise.quantidade_pessoas)
			return redirect('/MostraAnalise/')
	else:
		form = FormAnaliseSensorial()
	return verificar(request, {'form':form}, "Fabricante/Analise.html" )

#Edita os dados do fábricante
def editaRed(request):
	return edita(request, FormFabricanteEditar)

#Edita os dados da análise
def editaAnalise(request, id):
	#pegando objeto do banco
	analise = get_object_or_404(AnaliseSensorial, id=id)
	verificacao_usuario(request, analise)
	_id_user = get_test(request)
	#comparando o usuario logado com o usuario da analise
	#se o usuário tentar acessar uma anaálise que não é dele,
	# irá ser direcionado a pagina principal
	if analise.user_id == _id_user:
		form = FormAnaliseSensorialEditar(request.POST, instance=analise)
		if form.is_valid() and request.method == 'POST':
			form.save()
			return redirect('/MostraAnalise/')
		else:
			form = FormAnaliseSensorialEditar(instance=analise)
			return verificar(request, {'form':form, 'analise':analise}, 'Fabricante/editarAnalise.html')
	else:
		return redirect('/Funcionalidades/')


#Deletando objeto do banco de dados
def deletar_analise(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	verificacao_usuario(request, analise)
	analise.delete()
	return redirect('/MostraAnalise/')

#Retorna as análises cadastradas
def retornaAnalises(request):
	idTeste = get_test(request)
	analise = AnaliseSensorial.objects.filter(user = idTeste)
	print(analise)
	#request.session['analises'] = analise
	if analise is None:
		return HttpResponse("<h1>Nenhuma Análise Cadastrada</h1>")
	else:	
		return verificar(request, {'analises': analise}, 'Fabricante/retornaAnalise.html')


def page_perguntas(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	verificacao_usuario(request, analise)
	perguntas = Pergunta.objects.filter(analise_id = id)
	form = FormInserirPerguntas()
	#print(perguntas)
	return verificar(request, {'perguntas':perguntas, 'id':id, 'form':form}, 'Fabricante/inserirPergunta.html')

def cadastrar_pergunta(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	form = FormInserirPerguntas(request.POST)


	if form.is_valid():
		pergunta = form.cleaned_data['pergunta']
		tipo = form.cleaned_data['tipo']

		if tipo == 'PHD':
			salvar = PerguntaHedonica.objects.create(analise_id = id, pergunta=pergunta)
			print(form.tipo)
		elif tipo == 'PSN':
			salvar = PerguntaSimNao.objects.create(analise_id=id, pergunta=pergunta)
			pass
		elif tipo == 'PDT':
			salvar = PerguntaDissertativa.objects.create(analise_id=id, pergunta=pergunta)
		else:
			salvar = PerguntaIntencaoCompra.objects.create(analise_id=id, pergunta=pergunta) 

		print(tipo)

		#pergunta.save()

	return page_perguntas(request, id)

