from django.shortcuts import render
from Fabricante.forms import *
from Fabricante.models import *
from Fabricante.views import *
from django.template.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
#O ID da analise é requerido 
def graficoTeste(request, id):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
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
    
    

