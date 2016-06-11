from django.shortcuts import render
from webpage.forms import *
from django.contrib.auth.models import User
from webpage.models import *
# Create your views here.
#Jogando o formulário para o html
def Fabricante_page_cadastro(request):
	form = FormFabricante()
	return render(request, "Fabricante.html", {"form":form})

def Provador_page_cadastro(request):
	form = FormProvador()
	return render(request, "Provador.html", {"form":form})

def Cadastro_principal_page(request):
	return render(request, "cadastro_principal.html")

def Cadastro_Fabricante(request):
	if request.method == 'POST':
		form = FormFabricante(request.POST)
		#Vendo se o formário com o resquest é válido, se for, ele salva no models, pois o form é uma extensão do model
		if form.is_valid():
			form.save()
	else:
		#Se o método não for POST, ele mostra um formulário em branco
		form = FormFabricante()

	return render(request, "Fabricante.html", {"form":form})
			
def Cadastro_Provador(request):
	if request.method == 'POST':
		form = FormProvador(request.POST)
		#Verificando se o formulário é válido
		if form.is_valid():
			form.save()
	else:
		form = FormProvador()

	return render(request, "Provador.html", {"form":form})
