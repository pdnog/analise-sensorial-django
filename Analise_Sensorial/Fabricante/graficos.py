from django.shortcuts import render
from Fabricante.forms import *
from Fabricante.models import *
from Fabricante.views import *
from django.template.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import math
import itertools
def paginaGraficosBooleanos(request, id):
    return verificar(request,{'id':id, 'booleano':True}, 'Fabricante/graficos.html')
def paginaGraficosIntencaoCompra(request, id):
    return verificar(request,{'id':id, 'intencaoCompra':True}, 'Fabricante/graficos.html')
def paginaGraficosHedonica(request, id):
    return verificar(request,{'id':id, 'hedonica':True}, 'Fabricante/graficos.html')
def paginaGraficosIdade(request, id):
    return verificar(request,{'id':id, 'idade':True}, 'Fabricante/graficos.html')
"""
#O ID da analise é requerido
#Gráfico do Sexo (Não utilizado ainda)
def graficoTeste(request, id):
    #Pegando os testes daquela análise
    #close("all")
    masculino = 0
    feminino = 0
    testes = Teste.objects.filter(analise = id)
    for teste in testes:
        if teste.provador:
            if teste.provador.sexo == "1":
                masculino +=1
            else:
                feminino += 1


    data = ((masculino, feminino), ('r', '#00FF33'), ('Masculino', 'Feminino'))
    xPositions = np.arange(len(data[0]))
    barWidth = 0.50  # Largura da barra

    _ax = plt.axes()  # Cria axes
    plt.clf()
    # bar(left, height, width=0.8, bottom=None, hold=None, **kwargs)
    _chartBars = plt.bar(xPositions, data[0], barWidth, color=data[1],
                         yerr=5, align='center')  # Gera barras

    for bars in _chartBars:
        # text(x, y, s, fontdict=None, withdash=False, **kwargs)
        _ax.text(bars.get_x() + (bars.get_width() / 2.0), bars.get_height() + 5,
                 bars.get_height(), ha='center')  # Label acima das barras

    _ax.set_xticks(xPositions)
    _ax.set_xticklabels(data[2])

    plt.xlabel('Sexo')
    plt.ylabel('Quantidade')
    plt.grid(True)
    plt.legend(_chartBars, data[2])

    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response

Esse método será utilizado para calcular a idade, pode ser utilizado
aqui, nos gráficos, como também para verificar se a análise sensorial é
para pessoas maiores de 18 anos
def calculaIdade(birthday):
    today = date.today()
    y = today.year - birthday.year
    if today.month < birthday.month or today.month == birthday.month and today.day < birthday.day:
        y -= 1
    return y

def graficoIdade(request, id):
    #close("all")
    zeroDoze = 0
    trezeVinte = 0
    vinteUmTrinta = 0
    trintaUmQuarenta = 0
    quarentaUmCinquenta =0
    cinquentaSessenta = 0
    maisSessenta = 0

    #Verifica as idades válidas
    valido = True
    testes = Teste.objects.filter(analise = id)
    for teste in testes:
        if teste.provador is not None:
            idade = calculaIdade(teste.provador.data_nascimento)
            if idade > 0:
                if idade >= 0 and idade <= 12:
                    zeroDoze +=1
                elif idade > 12 and idade <= 20:
                    trezeVinte +=1
                elif idade > 20 and idade <= 30:
                    vinteUmTrinta +=1
                elif idade > 30 and idade <= 40:
                    trintaUmQuarenta += 1
                elif idade > 40 and idade <= 50:
                    quarentaUmCinquenta += 1
                elif idade > 50 and idade <= 60:
                    cinquentaSessenta += 1
                elif idade > 60:
                    maisSessenta += 1
            else:
                valido = False


    labels = '0 a 12 anos','13 a 20 anos','21 a 30 anos','31 a 40 anos', '41 a 50 anos', '51 a 60 anos','60 > anos'
    fracs=[zeroDoze, trezeVinte, vinteUmTrinta, trintaUmQuarenta,
        quarentaUmCinquenta, cinquentaSessenta, maisSessenta]
    explode = (0,0,0,0,0,0,0)
    pie = plt.pie(fracs, explode=explode, labels=labels, shadow=True, autopct='%1.1f%%',startangle=90)
    plt.clf()
    plt.legend(pie[0], labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response
"""
def graficoPerguntasBolleanas(request, id):
    #close("all")
    respostasBooleanas = Boolean.objects.filter(pergunta = id)
    
    sim = 0
    nao = 0
    for i in respostasBooleanas:
        if i.tipo=="PSN":
            if i.resposta == 1:
                sim += 1
            else:
                nao += 1
    data = ((nao, sim), ('r', '#00FF33'), ('Não', 'Sim'))
    xPositions = np.arange(len(data[0]))
    barWidth = 0.50  # Largura da barra

    _ax = plt.axes()  # Cria axes
    #isso apaga o cache, pras figuras não se sobrescreverem
    plt.clf()
    #plt.yticks(range(0,10))
    #Isso aqui é para o gráfico começar a partir da coordenada (0,0)
    low = min(data[0])
    high = max(data[0])
    plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
    #Isso aqui remove a parte de baixo do gráfico, os números que ficariam ali
    plt.tick_params(axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
    # bar(left, height, width=0.8, bottom=None, hold=None, **kwargs)
    _chartBars = plt.bar(xPositions, data[0], barWidth, color=data[1],
                         yerr=5, align='center')  # Gera barras

    for bars in _chartBars:
        # text(x, y, s, fontdict=None, withdash=False, **kwargs)
        _ax.text(bars.get_x() + (bars.get_width() / 2.0), bars.get_height() + 5,
                 bars.get_height(), ha='center')  # Label acima das barras

    _ax.set_xticks(xPositions)
    _ax.set_xticklabels(data[2])
    plt.ylabel('Pergunta Booleana')
    plt.xlabel('Resposta')
    #plt.ylabel('Quantidade')
    plt.grid(True)
    plt.legend(_chartBars, data[2])

    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response

def graficoHedonica(request, id):
    #close("all")
    respostasHedonicas = Hedonica.objects.filter(pergunta = id)
    pergunta = Pergunta.objects.get(pk=id)
    testes = Teste.objects.filter(analise = pergunta.analise)
    desgosteiExtremamente = 0
    desgosteiMuito = 0
    desgosteiModeradamente = 0
    desgosteiLigeiramente = 0
    neutro = 0
    gosteiLigeiramente = 0
    gosteiModeradamente = 0
    gosteiMuito = 0
    gosteiExtremamente = 0
    contadorProvador = 0
    for teste in testes:
        if teste.provador is not None:
            contadorProvador += 1
    
    
    for i in respostasHedonicas:
        if i.tipo=="PHD":
            if i.resposta == 1:
                desgosteiExtremamente +=1
            elif i.resposta == 2:
                desgosteiMuito += 2
            elif i.resposta == 3:
                desgosteiModeradamente += 3
            elif i.resposta == 4:
                desgosteiLigeiramente += 4
            elif i.resposta == 5:
                neutro += 5
            elif i.resposta == 6:
                gosteiLigeiramente += 6
            elif i.resposta == 7:
                gosteiModeradamente += 7
            elif i.resposta == 8:
                gosteiMuito += 8
            elif i.resposta == 9:
                gosteiExtremamente += 9
    aceitacao = []
    aceitacao.append((desgosteiExtremamente + desgosteiMuito + desgosteiModeradamente+ desgosteiLigeiramente+
               neutro+ gosteiLigeiramente+ gosteiModeradamente+ gosteiMuito + gosteiExtremamente)/contadorProvador)
    cor = ('r')
    data = (aceitacao, cor, "Aceitação")
    barWidth = 10  # Largura da barra
    xPositions = np.arange(len(data[0]))
    _ax = plt.axes()  # Cria axes
    _ax.set_yticks(np.arange(0, 9, 1))
    plt.clf()
    plt.tick_params(axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
    
    _chartBars = plt.bar(xPositions, data[0], barWidth, alpha=0.8, color=data[1],
                         yerr=2, align='center')  # Gera barras
    
    label = 'batata'
    for bars in _chartBars:
        # text(x, y, s, fontdict=None, withdash=False, **kwargs)
        _ax.text(bars.get_x() + (bars.get_width() / 2), bars.get_height()+5, label,
                  ha='center')  # Label acima das barras

    _ax.set_xticks(aceitacao)
    _ax.set_xticklabels(data[2])
    _ax.set_title('Gráficos da Escala Hedônica')
    plt.ylabel('Aceitação Hedonica: ' + str(data[0]))
    plt.grid(True)
    

    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response

def graficoIntencaoCompra(request, id):
    #close("all")
    respostasIntencao = IntencaoCompra.objects.filter(pergunta = id)
    pergunta = Pergunta.objects.get(pk=id)
    testes = Teste.objects.filter(analise = pergunta.analise)
    certamenteNao = 0
    possivelmenteNao = 0
    talvez = 0
    certamenteSim = 0
    possivelmenteSim = 0
    contadorProvador = 0
    for teste in testes:
        if teste.provador is not None:
            contadorProvador += 1
    
    for i in respostasIntencao:
        if i.tipo=="PIC":
            if i.resposta == 1:
                certamenteNao +=1
            elif i.resposta == 2:
                possivelmenteNao +=1
            elif i.resposta == 3:
                talvez += 1
            elif i.resposta == 4:
                possivelmenteSim += 1
            elif i.resposta == 5:
                certamenteSim += 1
                
    context = (certamenteNao, possivelmenteNao,talvez, possivelmenteSim, certamenteSim)
    cor = ('#ff00cb','#873c43','#643c87', '#3c8784','#f4f4f4')
    label = ('Certamente Não', 'Possivelmente Não', 'Talvez', 'Possivelmente Sim', 'Certamente Sim')
        
    data = (context, cor, label)
    
    
    xPositions = np.arange(len(data[0]))
    barWidth = 0.50  # Largura da barra

    _ax = plt.axes()  # Cria axes
    
    
    plt.clf()
    
    plt.tick_params(axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
    
    low = min(data[0])
    high = max(data[0])
    plt.ylim([math.ceil(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
    
    _chartBars = plt.bar(xPositions, data[0], barWidth, color=data[1],
                         yerr=5, align='center')  # Gera barras

    for bars in _chartBars:
        
        _ax.text(bars.get_x() + (bars.get_width() / 2.0), bars.get_height() + 5,
                 bars.get_height(), ha='center')  # Label acima das barras

    _ax.set_xticks(xPositions)
    _ax.set_xticklabels(data[2])

    #plt.xlabel('Sexo')
    plt.ylabel('Intenção de Compra')
    plt.grid(True)
    plt.legend(_chartBars, data[2])
    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response

def excel(request, id):
    import django_excel as excel
    import numpy as np
    import math
    lista = []
    aux=[]
    analise = AnaliseSensorial.objects.get(pk = id)
    perguntas = Pergunta.objects.filter(analise=analise.id)
    
    for pergunta in perguntas:  
        aux.append(pergunta.pergunta)
    
    for pergunta in perguntas:
        if pergunta.tipo == 'PIC':
            respostaIntencao = excelRetornaRespostas(IntencaoCompra,'PIC',id)
            lista.append(respostaIntencao)
        elif pergunta.tipo == 'PSN':
            respostaBoolean = excelRetornaRespostas(Boolean, 'PSN', id)
            lista.append(respostaBoolean)
        elif pergunta.tipo == 'PHD':
            respostaHedonica = excelRetornaRespostas(Hedonica, 'PHD', id)
            lista.append(respostaHedonica)
    lista = list(itertools.zip_longest(*lista))
    lista.append(aux)
    return excel.make_response_from_array(lista, 'xls')
def excelRetornaRespostas(tipoPergunta, sigla,id):
    analise = AnaliseSensorial.objects.get(pk = id)
    perguntas = Pergunta.objects.filter(analise=analise.id)
    respostas = []

    

    for pergunta in perguntas:
        
        if pergunta.tipo == sigla:                
                respostasTipo = tipoPergunta.objects.filter(pergunta = pergunta.id)
                for i in respostasTipo:
                    respostas.append(i.resposta)
    return respostas

"""
def excel(request, id):
    import django_excel as excel
    cont = 0
    list = []
    resposta = Resposta.objects.filter(analise=id)
    pergunta = Pergunta.objects.filter(analise=id)
    dicionarioRespostas = []
    a = []
    for i in pergunta:    
        if i.tipo == "PSN":
            boolean = Boolean.objects.filter(analise = id)
            for j in boolean:
                r = "Não"
                if j.resposta == 1:
                    r = "Sim"            
                a.append(r)
        if i.tipo == "PHD":
            
            hedonica = Hedonica.objects.filter(analise = id)
            for j in hedonica: 
                r = j.resposta           
                a.append(str(r))
        if i.tipo == "PIC":
            
            intencao = IntencaoCompra.objects.filter(analise = id)
            for j in intencao:            
                a.append(str(j.resposta))
        list.append(a) 
    for i in resposta:
-        cont+=1
-        
-        dicionarioRespostas.append(cont)
-   
    
        
    return excel.make_response_from_array(list, 'xls')  """