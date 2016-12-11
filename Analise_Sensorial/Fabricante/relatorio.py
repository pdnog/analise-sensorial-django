 # Create your views here.
import csv
#from reportlab.pdfgen import canvas
from io import BytesIO
#from reportlab.lib.pagesizes import letter, A4
#from random import randint
#from io import StringIO
#from Fabricante.metodos import transcricao_numero_letra
from django.http import HttpResponse
from Fabricante.models import *
from django.shortcuts import redirect, get_object_or_404

#Relatorio
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

#Gráficos
from reportlab.graphics.shapes import Drawing, Rect, String, Group, Line
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib import colors

def put_string(dictionary):
	label = '<font size=%s>%s</font>' % (dictionary['size'], dictionary['text'])
	dictionary['elements'].append(Paragraph(label, dictionary['styles'][dictionary['style']]))
	dictionary['elements'].append(Spacer(1, dictionary['spacer']))


#Método certo
def relatorio_final(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

	#Iniciando variáveis importantes
	buff = BytesIO()

	#Criando arquivos com as dimensões de margem
	arquivo = SimpleDocTemplate(buff, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=18)
	elements = []

	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='centered', alignment=TA_JUSTIFY))
	styles.add(ParagraphStyle(name='body', alignment=TA_JUSTIFY, fontSize=10))

	#Iniciando um dicionário de dados sobre o pdf
	dictionary = {'analise':analise, 'elements':elements, 'styles':styles}

	#Renderizando o título do documento
	dictionary['size'] = '20'
	dictionary['text'] = 'Relatório sobre a analise sensorial: ' + str(analise.nome)
	dictionary['style'] = 'title'
	dictionary['spacer'] = 20
	put_string(dictionary)
	#----------------------------------------------------------------------------------

	#Renderizando informações sobre a análise
	dictionary['size'] = '14'
	dictionary['spacer'] = 12
	dictionary['style'] = 'BodyText'

	dictionary['text'] = 'Nome: ' + str(analise.nome)
	put_string(dictionary)

	dictionary['text'] = 'Descrição: ' + str(analise.descricao)
	put_string(dictionary)

	dictionary['text'] = 'Quantidade de provadores: ' + str(analise.quantidade_pessoas)
	put_string(dictionary)

	dictionary['text'] = 'Quantidade de amostras: ' + str(analise.quantidade_amostras)
	put_string(dictionary)

	dictionary['text'] = 'Fabricante: ' + str(analise.user.first_name)
	put_string(dictionary)
	#-----------------------------------------------------------------------------------





	arquivo.build(elements)
	response.write(buff.getvalue())
	buff.close()
	return response
