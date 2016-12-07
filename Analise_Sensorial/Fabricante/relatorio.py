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

#Esse método não tá funcionando
def relatorio_final(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)

	doc = SimpleDocTemplate("relatorio.pdf", pagesize=letter,
							rightMargin=72, leftMargin=72,
							topMargin=72, bottomMargin=18)


	Story=[]
	magName = "Isso é um relatório."
	issueNum = 12

	formatted_time = time.ctime()
	full_name = "João Pedro Limão"

	styles=getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	ptext = '<font size=12>%s</font>' % formatted_time

	Story.append(Paragraph(ptext, styles["Normal"]))
	Story.append(Spacer(1, 12))
	"""#Estilo do parágrafo
	styles = getSampleStyleSheet()

	ParaStyle = styles["Normal"]
	ParaStyle.spaceBefore = 0.2 * cm
	ParaStyle.alignment = TA_JUSTIFY

	buffer = BytesIO()
	page = canvas.Canvas(buffer, pagesize=A4)
	page.setFont('Helvetica-Bold', 20)

	#Criando variaveis
	#HORIZONTAL
	horizontal = 30
	#VERTICAL
	vertical = 750

	p = Paragraph('Isso é um pequeno teste', ParaStyle)
	p.drawOn(page, 1 * cm, 1* cm)
	#page.drawString(0, 75, "Isso aqui é uma grande frase para saber se vai passar da margem")
	paga.drawString(0,200,p)
	page.save()
	pdf = buffer.getvalue()
	buffer.close()"""
	doc.build(Story)

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
	return response
