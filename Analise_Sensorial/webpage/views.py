from django.shortcuts import render
from webpage.forms import *
from django.contrib.auth.models import User
from webpage.models import *
# Create your views here.

def Fabricante_page_cadastro(request):
	form = FormFabricante2()
	return render(request, "Fabricante.html", {"form":form})

def Provador_page_cadastro(request):
	return render(request, "Provador.html")

def Cadastro_principal_page(request):
	return render(request, "cadastro_principal.html")

def Cadastro_Formulario(request):
	if request.method == 'POST':
		form = FormFabricante2(request.POST)
		#Vendo se o formário com o resquest é válido, se for, ele salva no models, pois o form é uma extensão do model
		if form.is_valid():
			form.save()
	else:
		#Se o método não for POST, ele mostra um formulário em branco
		form = FormFabricante2()

	return render(request, "Fabricante.html", {"form":form})
			




