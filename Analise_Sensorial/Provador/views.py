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


def page_resposta(request, id):
    analise = get_object_or_404(AnaliseSensorial, id=id)
    perguntas = Pergunta.objects.filter(analise_id=id)
    id_provador = get_test(request)

    # PRECISA-SE RECEBER O ID DO PROVADOR QUE ESTÁ FAZENDO O TESTE
    # RECENBENDO O CONTROLE DE LAYOUT
    controle = request.GET['controle']

    if controle == 'True':
        respostas = {}

        # RECEBENDO AMOSTRAS, TESTES E PROVADOR PARA CRIAR A NOVA PERGUNTA
        id_amostra = request.GET['amostra']
        provador = Provador.objects.get(user_id=id_provador)

        # INICIANDO VARIÁVEL
        amostra = None
        hedonica = []
        intencao_compra = []
        dissertativa = []
        boolean = []
        lista_respostas = []

        try:
            amostra = Amostra.objects.get(numero=id_amostra, analise_id=id)
            print("That's ok, have one 'amostra' with this pk")
        except Exception as e:
            # TRATANDO EXCESSÕES NO QUAL O USUÁRIO DIGITE O NÚMERO DE UMA AMOSTRA QUE
            # NÃO HÁ NO BANCO DE DADOS
            print("Do have not any 'amostra' with this pk")

        try:
            teste = Teste.objects.get(id=amostra.teste.id)
            print(teste)
            print(provador)
            # print(amostra.teste.id)
            #teste.provador.id = id_provador
            print("That's ok, have one 'teste' with this pk")
        except Exception as e:
            print(
                "Do have not any 'teste' with this pk or not have 'amostra' to this 'teste'")
            #print(str(amostra.teste.id) + " - no erro")

        # print(amostra.id)

        for pergunta in perguntas:
            lista_respostas.append(
                (
                    str(analise.id),
                    str(amostra.id),
                    str(teste.id),
                    str(pergunta.tipo),
                    str(pergunta.id)
                )
            )

        # INSERINDO RESPOSTAS NO BANCO DE DADOS
        cursor = connection.cursor()
        # ESTÁ DANDO ERRO QUANDO TENTO INSERIR DA MANEIRA CERTA
        query = "INSERT INTO fabricante_resposta (analise_id, amostra_id, teste_id, tipo, pergunta_id) VALUES (%s, %s, %s, %s, %s);"
        cursor.executemany(query, lista_respostas)

        # SEGUNDA PARTE
        respostas_id_and_perguntas_id = Resposta.objects.filter(
            analise_id=analise.id, amostra_id=amostra.id)

        # Primeiro tenho que pegar o id da resposta e o pergunta_id da tabela resposta
        # Então eu pego as perguntas de acordo com o pergunta_id do select nas respostas
        # Então eu crio 4 novos inserts, um pra cada tipo e os cadastro sem criar objetos
        # RECEBENDO TODOS OS FORMULÁRIOS
        for resposta in respostas_id_and_perguntas_id:
            id = resposta.id
            pergunta_pk = resposta.pergunta.id
            tipo = resposta.tipo

            if str(pergunta_pk) in request.GET:
                # RECEBENDO OS DADOS DO FORMULÁRIO
                resposta_do_provador = request.GET['' + str(pergunta_pk)]
                print(resposta_do_provador)
                if tipo == "PHD":
                    hedonica.append((str(id), str(resposta_do_provador)))
                elif tipo == "PSN":
                    print(resposta_do_provador)
                    print("É um teste")
                    if(resposta_do_provador == 'True'):
                        boolean.append((str(id), 0))
                    else:
                        boolean.append((str(id), 1))
                elif tipo == "PDT":
                    dissertativa.append((str(id), str(resposta_do_provador)))
                else:
                    intencao_compra.append(
                        (str(id), str(resposta_do_provador)))

        # INSERT NO MODEL HEDONICA
        try:
            query_PHD = "INSERT INTO fabricante_hedonica (resposta_ptr_id, resposta) VALUES (%s, %s)"
            cursor.executemany(query_PHD, hedonica)
        except Exception as e:
            print("Erro no formato de dado da resposta do 'fabricante_hedonica'")
            print(str(e))

        # INSERT NO MODEL BOOLEAN
        try:
            query_PSN = "INSERT INTO fabricante_boolean (resposta_ptr_id, resposta) VALUES (%s, %s)"
            cursor.executemany(query_PSN, boolean)
        except Exception as e:
            print("Erro no formato de dado da resposta do 'fabricante_boolean'")
            print(str(e))

        # INSERT NO MODEL DISSERTATIVA
        try:
            query_PDT = "INSERT INTO fabricante_dissertativa (resposta_ptr_id, resposta) VALUES (%s, %s)"
            cursor.executemany(query_PDT, dissertativa)
        except Exception as e:
            print("Erro no formato de dado da resposta do 'fabricante_dissertativa'")
            print(str(e))

        # INSERT NO MODEL INTENCAOCOMPRA
        try:
            query_ITC = "INSERT INTO fabricante_intencaocompra (resposta_ptr_id, resposta) VALUES (%s, %s)"
            cursor.executemany(query_ITC, intencao_compra)
        except Exception as e:
            print("Erro no formato de dado da resposta do 'fabricante_intencaocompra'")
            print(str(e))

        return redirect('/Home_Provador/')

    # QUANDO FOR FALSO ELE IRÁ INICIAR O TESTE SENSORIAL
    else:
        dicionario = formularios(perguntas, id)

    # Tenho que ver como concatenar várias perguntas de tipos diferentes
    return verificar(request, dicionario, 'Provador/responder_analise.html')


def page_respostas(request, id):
    # Conexão 01
    analise = get_object_or_404(AnaliseSensorial, id=id)
    # Conexão 02
    perguntas = Pergunta.objects.filter(analise_id=id)
    id_provador = get_test(request)

    # PRECISA-SE RECEBER O ID DO PROVADOR QUE ESTÁ FAZENDO O TESTE
    # RECENBENDO O CONTROLE DE LAYOUT
    controle = request.GET['controle']

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

        return redirect('/Home_Provador/')
    else:
        dicionario = formularios(perguntas, id)

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
