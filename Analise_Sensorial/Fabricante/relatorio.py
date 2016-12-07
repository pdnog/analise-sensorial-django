# Create your views here.
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from random import randint
from io import StringIO
from Fabricante.metodos import transcricao_numero_letra
from django.http import HttpResponse
from Fabricante.models import *
from django.shortcuts import redirect, get_object_or_404

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


#Método certo
def relatorio_final(request, id):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

	buff = BytesIO()

	arquivo = SimpleDocTemplate(buff, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

	elements = []

	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='centered', alignment=TA_JUSTIFY))

	#Renderizando um paragrafo no documento
	label = 'O que aconteceria se colocar uma label enorme para ver como fica renderizada na tela do arquivo pdf.'
	elements.append(Paragraph(label, styles['centered']))
	
	arquivo.build(elements)
	response.write(buff.getvalue())
	buff.close()
	return response
