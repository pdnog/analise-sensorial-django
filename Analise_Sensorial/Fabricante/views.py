#NEED MORE SPACE
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from Fabricante.forms import *
from Fabricante.models import *
from webpage.forms import *
from webpage.views import *
from django.contrib.auth.decorators import login_required
from Fabricante.metodos import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
			analise.possui_amostras = True
			analise.ativado = False
			#Salvei
			analise.save()
			#Criando testes
			print (analise.id)
			print (analise.quantidade_pessoas)
			#LEMBRE_SEEEEEEEE
			#VIU?
			#FILHA DA MÂE ESSE ERRO
			#PASSEI 1 HORA PARA DESCOBRIR
			#NÃO FAÇA CAGADA
			#PELO AMOR DE DEUS OU SEJA LÁ SUA RELIGIÃO
			#GERAR TESTES SEMPRE TERÁ QUE VIR ANTES DE GERAR AMOSTRAS
			gerar_testes(analise.id, analise.quantidade_pessoas)
			gerar_amostras(analise.id, analise.quantidade_amostras)
			#--------------------------------------------------------------
			#--------------------------------------------------------------
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

	#Mostra 10 análises do que foi retornado pelo banco de dados
	paginacao = Paginator(analise,6)

	#Só para utilizar o get ?pagina=1 na url
	pagina = request.GET.get('pagina')
	try:
		analises = paginacao.page(pagina)
	except PageNotAnInteger:
		analises = paginacao.page(1)
	except EmptyPage:
		analises = paginacao.page(paginacao.num_pages)
	#print(analise)
	#request.session['analises'] = analise
	if analise is None:
		return HttpResponse("<h1>Nenhuma Análise Cadastrada</h1>")
	else:
		return verificar(request, {'analises': analises}, 'Fabricante/retornaAnalise.html')


def page_perguntas(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	verificacao_usuario(request, analise)
	pergunta = Pergunta.objects.filter(analise_id = id)
	paginacao = Paginator(pergunta,10)
	#Só para utilizar o get ?pagina=1 na url
	pagina = request.GET.get('pagina')
	try:
		perguntas = paginacao.page(pagina)
	except PageNotAnInteger:
		perguntas = paginacao.page(1)
	except EmptyPage:
		perguntas = paginacao.page(paginacao.num_pages)
	form = FormInserirPerguntas()
	tipo = {}
	for i in pergunta:
		if i.tipo=="PIC":
			tipo[i] = []
			tipo[i].append('Intenção Compra')
		if i.tipo=="PSN":
			tipo[i] = []
			tipo[i].append('Sim ou Não')
		if i.tipo=="PHD":
			tipo[i] = []
			tipo[i].append('Hedônica')
		if i.tipo=="PDT":
			tipo[i] = []
			tipo[i].append('Dissertativa')
	return verificar(request, {'perguntas':perguntas, 'id':id,
							 'form':form, 'tipo':tipo}, 'Fabricante/inserirPergunta.html')

def cadastrar_pergunta(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	form = FormInserirPerguntas(request.POST)

	if form.is_valid():
		pergunta = form.cleaned_data['pergunta']
		tipo = form.cleaned_data['tipo']

		objeto = Pergunta.objects.create(analise_id = id,
			pergunta = pergunta, tipo = tipo)

	return redirect('/Perguntas/' + id)

def editarPergunta(request, id):
	pergunta = get_object_or_404(Pergunta, id = id)
	analise = pergunta.analise
	form = FormInserirPerguntas(request.POST, instance=pergunta)
	if  request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('/Perguntas/'+str(analise.id))
	else:
		form = FormInserirPerguntas(instance = pergunta)
	return verificar(request, {'form':form,'id':pergunta.id,'analiseID':analise.id}, 'Fabricante/editarPergunta.html')

def deletarPergunta(request, id):
	pergunta = get_object_or_404(Pergunta, id = id)
	analise = pergunta.analise
	pergunta.delete()
	return redirect('/Perguntas/'+str(analise.id))
