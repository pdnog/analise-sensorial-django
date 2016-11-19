# Create your views here.
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from random import randint
from io import StringIO 
from Fabricante.metodos import transcricao_numero_letra
from django.http import HttpResponse
from Fabricante.models import *
from django.shortcuts import redirect, get_object_or_404

from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet

def relatorio_final(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)

	#Estilo do parágrafo
	styles = getSampleStyleSheet()

	ParaStyle = copy.deepcopy(styles["Normal"])
	ParaStyle.spaceBefore = 0.2 * cm
	ParaStyle.alignment = TA_JUSTIFY

	buffer = BytesIO()
	page = canvas.Canvas(buffer, pagesize=letter)
	page.setFont('Helvetica-Bold', 20)

	#Criando variaveis
	#HORIZONTAL
	horizontal = 30
	#VERTICAL
	vertical = 750

	p = Paragraph('Isso é um pequeno teste', ParaStyle)
	p.drawOn(page, 1 * cm, 1* cm)
	page.save()
	pdf = buffer.getvalue()
	buffer.close()

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
	response.write(pdf)
	return response