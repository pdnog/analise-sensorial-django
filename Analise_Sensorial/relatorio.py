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

#Usando para o parágrafo 
from reportlab.platypus import (
    BaseDocTemplate, 
    PageTemplate, 
    Frame, 
    Paragraph
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)

def stylesheet():
    styles= {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
        ),
    }
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=purple,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=yellow,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    return styles

def relatorio_final(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)

	buffer = BytesIO()
	page = canvas.Canvas(buffer, pagesize=letter)
	page.setFont('Helvetica-Bold', 20)

	#Criando variaveis

	#HORIZONTAL
	horizontal = 30
	#VERTICAL
	vertical = 750

	"""#page.drawString(horizontal, 750, "Relatório da análise '" + str(analise.nome) + "'")
	#page.stringWidth("Relatório da análise '" + str(analise.nome) + "'", "Helvetica", 16, encoding=None)
	page.setTitle("Relatório da análise '" + str(analise.nome) + "'")
	page.setFont('Helvetica-Bold', 16)
	page.drawString(horizontal, 700, "Informações sobre a analise: ")

	page.setFont('Helvetica', 16)
	page.drawString(horizontal, 670, "NOME: " + str(analise.nome))
	page.drawString(horizontal, 640, "DESCRIÇÃO: " + str(analise.descricao))
	page.drawString(horizontal, 610, "QUANTIDADE DE PROVADORES: " + str(analise.quantidade_pessoas))
	page.drawString(horizontal, 580, "QUANTIDADE DE AMOSTRAS: " + str(analise.quantidade_amostras))
	page.drawString(horizontal, 550, "FABRICANTE: " + str(analise.user.username))

	
	objeto = page.beginText()
	objeto.setTextOrigin(20, 400)
	objeto.setFont('Helvetica-Bold', 16)
	objeto.setLeading(20)
	objeto.textLines(texto)

	page.drawText(objeto)"""

	page.drawString(horizontal, 700,"<p>Testando 1, 2, 3 <p>")

	Paragraph("Isso é apenas um teste.", 'title')


	page.save()

	pdf = buffer.getvalue()
	buffer.close()

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
	response.write(pdf)
	return response


