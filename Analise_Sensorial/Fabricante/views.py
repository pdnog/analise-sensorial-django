from django.shortcuts import render
from django.shortcuts import redirect
from Fabricante.forms import *
# Create your views here.
def Funcionalidades(request):
	return verificar(request, {}, "Fabricante/Funcoes.html")

#Pegando a sessão feita
def get_name(request):
	nome = request.session.get('nome')
	return nome

#Verificãção de login- toda página criada será preciso chama-la
def  verificar(request, dicionario, html):
	nome = get_name(request)
	dicionario['nome_usuario'] = nome
	if nome is not None:
		return render(request, html, dicionario)
	else:
		return redirect('/')


def FormDadosAnalise_Page(request):
	form = FormDadosAnalise()
	return verificar(request, {'form':form}, "Fabricante/Analise.html")

def CadastrarFormAnalise(request):
	form = FormDadosAnalise(request.POST)

	if form.is_valid():
		pass
	else:
		return verificar(request, {'form':form}, "Fabricante/Analise.html")