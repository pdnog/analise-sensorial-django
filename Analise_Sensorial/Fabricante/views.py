#NEED MORE SPACE
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from Fabricante.forms import *
from Fabricante.models import *
from webpage.forms import *
from webpage.views import edita, get_test, verificar, get_name
from django.contrib.auth.decorators import login_required
from Fabricante.metodos import *

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
	return verificar(request, {'analise':id, 'numeros_presentes':analise.possui_amostras}, 
		"Fabricante/numeros_page.html")

def gerar_amostras_action(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	gerar_amostras(id, analise.quantidade_pessoas, analise.quantidade_amostras)
	
	#gerando_amostras(id, analise.quantidade_amostras)
	analise.possui_amostras = True
	analise.save()
	return redirect('/MostraAnalise/')

#Método não terminado
"""def Gerar_numeros(request, id):
	analise = get_object_or_404(Analise_Dados_Pessoais, id=id) 
	form = FormDadosNumerosAleatorios(request.POST)

	if form.is_valid():
		formulario = form.save(commit=False)
		amostras = form.cleaned_data['quantidade_amostras']
		pessoas = form.cleaned_data['quantidade_pessoas']
		analise.Possui_numeros = True
		analise.save()
		formulario.analise_id = analise.id
		formulario.save()
		#Método encontrado no arquivo 'gerador.py'
		salvar_numeros(analise.id, pessoas, amostras)
		return redirect('/MostraAnalise/')

	form = FormDadosNumerosAleatorios()
	return verificar(request, {'form':form}, 'Fabricante/Analise.html')

"""

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

			#gerar_amostras(analise.id, analise.quantidade_pessoas, analise.quantidade_amostras)
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
	_id_user = get_test(request)
	#comparando o usuario logado com o usuario da analise
	#se o usuário tentar acessar uma anaálise que não é dele, irá ser direcionado a pagina principal
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
	analise.delete()
	return redirect('/MostraAnalise/')

#Retorna as análises cadastradas
def retornaAnalises(request):
	idTeste = get_test(request)
	analise = AnaliseSensorial.objects.filter(user = idTeste)
	if analise is None:
		return HttpResponse("<h1>Nenhuma Análise Cadastrada</h1>")
	else:	
		return verificar(request, {'analise': analise}, 'Fabricante/retornaAnalise.html')

	 
