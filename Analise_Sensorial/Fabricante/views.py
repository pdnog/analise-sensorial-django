#NEED MORE SPACE
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from Fabricante.forms import *
from webpage.forms import FormFabricante
from Fabricante.models import Analise_Dados_Pessoais
from webpage.views import edita, get_test, verificar, get_name

# Create your views here.
def Funcionalidades(request):
	return verificar(request, {}, "Fabricante/Funcoes.html")

def FormDadosAnalise_Page(request):
	form = FormDadosAnalise()
	return verificar(request, {'form':form}, "Fabricante/Analise.html")

def CadastrarFormAnalise(request):
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
		return HttpResponseRedirect('/Funcionalidades/')
	else:
		return FormDadosAnalise_Page(request)

#Edita os dados do fábricante
def editaRed(request):
	return edita(request, FormFabricante)

#Edita os dados da análise
def editaAnalise(request):
	return edita(request, Analise_Dados_Pessoais)

#Retorna as análises cadastradas
def retornaAnalises(request):
	idTeste = get_test(request)
	analise = Analise_Dados_Pessoais.objects.filter(user = idTeste)
	if analise is None:
		return HttpResponse("<h1>Nenhuma Análise Cadastrada</h1>")
	else:	
		return verificar(request, {'analise': analise}, 'retornaAnalise.html')
	

