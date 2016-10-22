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
#O ID da analise é requerido
def graficoTeste(request, id):
    #Pegando os testes daquela análise

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

"""Esse método será utilizado para calcular a idade, pode ser utilizado
aqui, nos gráficos, como também para verificar se a análise sensorial é
para pessoas maiores de 18 anos"""
def calculaIdade(birthday):
    today = date.today()
    y = today.year - birthday.year
    if today.month < birthday.month or today.month == birthday.month and today.day < birthday.day:
        y -= 1
    return y

def graficoIdade(request, id):
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
    plt.legend(pie[0], labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response

def graficoPerguntasBolleanas(request, id):
    respostasBooleanas = Boolean.objects.filter(analise = id)
    sim = 0
    nao = 0
    for i in respostasBooleanas:
        if i.tipo=="PSN":
            if i.resposta == True:
                sim +=1
            else:
                nao += 1
    data = ((nao, sim), ('r', '#00FF33'), ('Não', 'Sim'))
    xPositions = np.arange(len(data[0]))
    barWidth = 0.50  # Largura da barra

    _ax = plt.axes()  # Cria axes

    # bar(left, height, width=0.8, bottom=None, hold=None, **kwargs)
    _chartBars = plt.bar(xPositions, data[0], barWidth, color=data[1],
                         yerr=5, align='center')  # Gera barras

    for bars in _chartBars:
        # text(x, y, s, fontdict=None, withdash=False, **kwargs)
        _ax.text(bars.get_x() + (bars.get_width() / 2.0), bars.get_height() + 5,
                 bars.get_height(), ha='center')  # Label acima das barras

    _ax.set_xticks(xPositions)
    _ax.set_xticklabels(data[2])

    plt.xlabel('Resposta')
    #plt.ylabel('Quantidade')
    plt.grid(True)
    plt.legend(_chartBars, data[2])

    canvas = FigureCanvas(plt.figure(1))
    response =  HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response
