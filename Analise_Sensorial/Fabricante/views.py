#NEED MORE SPACE
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from Fabricante.forms import *
from Fabricante.models import *
from webpage.forms import FormFabricante
from Fabricante.models import Analise_Dados_Pessoais
from webpage.views import edita, get_test, verificar, get_name
from django.contrib.auth.decorators import login_required

# Create your views here.
def Funcionalidades(request):
	return verificar(request, {}, "Funcoes.html")

def FormDadosAnalise_Page(request):
	form = FormDadosAnalise()
	return verificar(request, {'form':form}, "Fabricante/Analise.html")

#Precisa aperfeiçoar esse método
#Quando o usuário cadastrar os números não aparecerá o botão de cadastrar números
def Gerar_numeros_page(request, id):
	form = FormDadosNumerosAleatorios()
	return verificar(request, {'form':form}, "Fabricante/numeros_page.html")

#Método não terminado
def Gerar_numeros(request, id):
	analise = get_object_or_404(Analise_Dados_Pessoais, id=id)
	form = FormDadosNumerosAleatorios(request.POST)

	if form.is_valid():
		form.save()
		amostras = form.cleaned_data['quantidade_amostras']
		pessoas = form.cleaned_data['quantidade_pessoas']


def CadastrarFormAnalise(request):
	if request.method == 'POST':
		form = FormDadosAnalise(request.POST)

		if form.is_valid():
			#Campo que diz: Espere, vou adicionar o usuário
			analise = form.save(commit=False)
			#Adicionei o usuário, que é obrigatório
			idTeste = get_test(request)
			usuario = User.objects.get(id = idTeste)	
			analise.user = usuario
			#Salvei
			analise.save()
			return redirect('/MostraAnalise/')
	else:
		form = FormDadosAnalise()
	return verificar(request, {'form':form}, "Fabricante/Analise.html" )

#Edita os dados do fábricante
def editaRed(request):
	return edita(request, FormFabricante)

#Edita os dados da análise
def editaAnalise(request, id):
	#pegando objeto do banco
	analise = get_object_or_404(Analise_Dados_Pessoais, id=id)
	_id_user = get_test(request)
	#comparando o usuario logado com o usuario da analise
	#se o usuário tentar acessar uma anaálise que não é dele, irá ser direcionado a pagina principal
	if analise.user_id == _id_user:
		form = FormDadosAnalise(request.POST, instance=analise)
		if form.is_valid() and request.method == 'POST':
			form.save()
			return redirect('/MostraAnalise/')
		else:
			form = FormDadosAnalise(instance=analise)
			return verificar(request, {'form':form, 'analise':analise}, 'Fabricante/editarAnalise.html')
	else:
		return redirect('/Funcionalidades/')


#Deletando objeto do banco de dados
def deletar_analise(request, id):
	analise = get_object_or_404(Analise_Dados_Pessoais, id=id)
	analise.delete()
	return redirect('/MostraAnalise/')

#Retorna as análises cadastradas
def retornaAnalises(request):
	idTeste = get_test(request)
	analise = Analise_Dados_Pessoais.objects.filter(user = idTeste)
	if analise is None:
		return HttpResponse("<h1>Nenhuma Análise Cadastrada</h1>")
	else:	
		return verificar(request, {'analise': analise}, 'Fabricante/retornaAnalise.html')


	 
