from django.shortcuts import render
from django.shortcuts import redirect
from Fabricante.forms import *
from webpage.forms import FormFabricante
# Create your views here.
def Funcionalidades(request):
	return verificar(request, {}, "Fabricante/Funcoes.html")

#Pegando a sessão feita
def get_name(request):
	nome = request.session.get('nome')
	return nome
#Pegando a sessão teste
def get_test(request):
	idTeste = request.session.get('teste')
	return idTeste

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

def editaRed(request):
	idTeste = get_test(request)
	usuario = User.objects.get(id = idTeste)	
	if request.method == "POST":
		#Uso o instance para instanciar o objeto para o formulário
		form = FormFabricante(request.POST, instance = usuario)
		if form.is_valid():
			form.save()
			#Falta colocar uma confirmação de "editou!"
			return render(request, "Fabricante/Funcoes.html")
	else:
		form = FormFabricante(instance=usuario)
	return verificar(request,{'form':form}, 'editar.html')

