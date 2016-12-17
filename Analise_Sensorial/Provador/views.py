from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from webpage.views import verificar, verificacao_usuario, get_test
from django.forms import formset_factory, BaseFormSet
from django.utils.functional import curry
from Fabricante.models import *
from django.db import connection, transaction
from django.core.exceptions import *
from Fabricante.forms import *


# Create your views here.
""" Renderização de paginas """
def home_provador(request):
    dicionario = {}
    analises = AnaliseSensorial.objects.filter(ativado=True)
    dicionario['analises'] = analises
    return verificar(request, dicionario, "Provador/home_provador.html")

# USADO PARA SABER QUANTAS PÁGINAS DE FORMULÁRIOS QUE IREMOS CRIAR
contador_amostras = 0
def page_respostas(request, id):
    # Conexão 01
    analise = get_object_or_404(AnaliseSensorial, id=id)
    # Conexão 02
    perguntas = Pergunta.objects.filter(analise_id=id)
    id_provador = get_test(request)

    # PRECISA-SE RECEBER O ID DO PROVADOR QUE ESTÁ FAZENDO O TESTE
    # RECENBENDO O CONTROLE DE LAYOUT
    controle = request.GET['controle']
    dicionario = formularios(perguntas, id)

    if controle == "True":

        # Recebendo amostra
        numero_amostra = request.GET['amostra']

        # Recuperando provador
        # Conexão 03
        provador = User.objects.get(id=id_provador)
        print(provador)

        # INICIANDO VARIÁVEL
        amostra = None
        teste = None
        hedonica = []
        intencao_compra = []
        dissertativa = []
        boolean = []
        lista_respostas = []

        try:
            # Conexão 04
            # Recuperando amostra e teste para cadastrar respsotas
            amostra = Amostra.objects.get(numero=numero_amostra, analise_id=id)
            print("That's ok, have one 'amostra' with this pk")
        except Exception as e:
            print("Do have not any 'amostra' with this pk")

            # Error: Amostra matching query does not exist.
            print(str(e))
            # Aqui seria bom renderizar uma página de 404

        try:
            # Conexão 05
            teste = Teste.objects.get(id=amostra.teste.id)
            teste.provador = provador
            teste.save()

        except Exception as e:
            #raise e
            print(e)

        # Para cada pergunta eu devo ter a resposta correspondente através do
        # ID
        try:
            for pergunta in perguntas:
                tipo = pergunta.tipo

                # Recebendo pergunta do template
                resposta_template = request.GET['' + str(pergunta.id)]

                # Conexão06
                if tipo == "PHD":
                    objeto = Hedonica.objects.create(
                        analise=analise,
                        teste=teste,
                        amostra=amostra,
                        pergunta=pergunta,
                        tipo=tipo,
                        resposta=resposta_template
                    )

                elif tipo == "PSN":
                    resposta = None
                    if(resposta_template == 'True'):
                        resposta = True
                    else:
                        resposta = False

                    objeto = Boolean.objects.create(
                        analise=analise,
                        teste=teste,
                        amostra=amostra,
                        pergunta=pergunta,
                        tipo=tipo,
                        resposta=resposta
                    )

                elif tipo == "PDT":
                    objeto = Dissertativa.objects.create(
                        analise=analise,
                        teste=teste,
                        amostra=amostra,
                        pergunta=pergunta,
                        tipo=tipo,
                        resposta=resposta_template
                    )
                else:
                    objeto = IntencaoCompra.objects.create(
                        analise=analise,
                        teste=teste,
                        amostra=amostra,
                        pergunta=pergunta,
                        tipo=tipo,
                        resposta=resposta_template
                    )
        except Exception as e:
            print(str(e))

        #Pegando variável global
        global contador_amostras
        contador_amostras += 1
        print('contador: ' + str(contador_amostras))

        if contador_amostras==analise.quantidade_amostras:
            contador_amostras = 0
            return redirect('/Home_Provador/')
        else:
            return verificar(request, dicionario, 'Provador/responder_analise.html')
    else:
        return verificar(request, dicionario, 'Provador/responder_analise.html')

""" Lógicas de sistema """
def formularios(perguntas, id):
    # CRIANDO VARIÁVEIS
    hedonica = []
    boolean = []
    intencao_compra = []
    descritiva = []

    for pergunta in perguntas:
        # CRIANDO OBJETOS PARA SEREM RENDERIZADOS PELO TEMPLATE
        object = Word(None, None, None)
        object.pergunta = pergunta.pergunta
        object.id = pergunta.id
        object.tipo = pergunta.tipo

        if pergunta.tipo == 'PHD':
            hedonica.append(object)
        elif pergunta.tipo == 'PSN':
            boolean.append(object)
        elif pergunta.tipo == 'PDT':
            descritiva.append(object)
        else:
            intencao_compra.append(object)

    # ADCIONANDO LISTAS NO DICIONÁRIO
    dicionario = {}
    dicionario['id'] = id
    dicionario['hedonica'] = hedonica
    dicionario['boolean'] = boolean
    dicionario['descritiva'] = descritiva
    dicionario['intencao_compra'] = intencao_compra

    return dicionario

""" Classes de concatenação """
# Classe usada para concatenar a pergunta com o input do formulário
class Word(object):
    """docstring Word"""

    def __init__(self, pergunta, tipo, id):
        self.pergunta = pergunta
        self.tipo = tipo
        self.id = id
