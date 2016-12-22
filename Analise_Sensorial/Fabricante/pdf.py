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
from reportlab.platypus.tables import Table, TableStyle
#Relatorio
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from Fabricante.number_page import *

def gerar_linhas_colunas(page, horizontal, vertical):
	for j in range(8):
			page.line(horizontal, 700, horizontal, 50)
			horizontal = horizontal + 100

	for j in range(21):
		page.line(5, vertical, 605, vertical)
		vertical = vertical - 50

def criando_estrutura2(request, id):
	analise = get_object_or_404(AnaliseSensorial, id=id)

	buffer = BytesIO()
	page = canvas.Canvas(buffer, pagesize=letter)
	page.setFont('Helvetica', 20)
	#Entre linhas deve ter 30px
	#Entre coluna deverá ter 70px
	for i in range(analise.quantidade_amostras):
		letra = str(transcricao_numero_letra(i))
		page.drawString(230, 750, "Números da amostra " + letra)

		#Declarando variáveis
		horizontal = 5
		vertical = 700

		gerar_linhas_colunas(page, horizontal, vertical)

		#Reiniciando as variáveis
		horizontal_numero = 10
		vertical_numero = 670
		contador = 0
		contador_pular_linha = 0
		#O número deve iniciar em um x que seja +10 do horizontal
		#O número deve iniciar em um y que seja -20 do vertical

		while contador<analise.quantidade_pessoas:

			for j in Amostra.objects.filter(analise_id=id, tipo=letra):
				contador = contador + 1
				page.drawString(horizontal_numero,
					vertical_numero, str(contador) + "- '" + str(j.numero) + "'")
				contador_pular_linha += 1
				horizontal_numero += 100

				if(contador_pular_linha == 6):
					horizontal_numero = 10
					vertical_numero -= 50
					contador_pular_linha = 0
					print(vertical_numero)

				if vertical_numero==20:
					page.showPage()
					page.setFont('Helvetica', 20)
					letra = str(transcricao_numero_letra(i))
					page.drawString(220, 750, "Continuação da amostra " + letra)
					#Variaveis para gerar linha e colunas
					horizontal = 5
					vertical = 700
					gerar_linhas_colunas(page, horizontal, vertical)
					#Variaveis para posição de numeros
					horizontal_numero = 10
					vertical_numero = 670

		page.showPage()
		page.setFont('Helvetica', 20)

	page.save()

	pdf = buffer.getvalue()
	buffer.close()

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="numeros_aleatorios.pdf"'
	response.write(pdf)
	return response

def imprimir_numeros(request):
	buffer = BytesIO()
	p = canvas.Canvas(buffer, pagesize=letter)
	# Dracw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(50, 700, "A")
	p.drawString(150, 700, "B")
	p.drawString(250, 700, "C")
	p.drawString(350, 700, "A")
	p.drawString(450, 700, "B")
	p.drawString(550, 700, "C")
	p.line(110, 0, 110, 655)
	p.line(210, 0, 210, 655)
	p.line(310, 0, 310, 655)
	p.line(410, 0, 410, 655)
	p.line(510, 0, 510, 655)

	vetor_verificacao = []
	vetor_A = []
	vetor_B = []
	vetor_C = []

	for i in range(180):
		#Criando um número aleatório
		number = randint(100, 999)

		#Verificando se ele já não foi selecionado
		while number in vetor_verificacao:
			number = randint(100, 999)

		#Condições de população de vetores
		if(i<60):
			vetor_A.append(number)
		elif(i>=60 and i<120):
			vetor_B.append(number)
		else:
			vetor_C.append(number)

		vetor_verificacao.append(number)


	line = 655
	p.line(0, line, 630, line)
	vertical = 640
	horizontal = 50
	for i in vetor_A:
		p.drawString(horizontal, vertical, str(i))
		vertical -= 20
		line -= 20
		p.line(0, line, 630, line)
		if vertical == 0:
			horizontal = 350
			vertical = 640

	vertical = 640
	horizontal = 150
	for i in vetor_B:
		p.drawString(horizontal, vertical, str(i))
		vertical -= 20
		if vertical == 0:
			horizontal = 450
			vertical = 640

	vertical = 640
	horizontal = 250
	for i in vetor_C:
		p.drawString(horizontal, vertical, str(i))
		vertical -= 20
		if vertical == 0:
			horizontal = 550
			vertical = 640



	# Close the PDF object cleanly.
	p.showPage()
	p.save()
	# Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="numeros_aleatorios.pdf"'
	response.write(pdf)
	return response

def criando_estrutura(request, id):
	analise = get_object_or_404(AnaliseSensorial,id=id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="numeros_aleatorios.pdf"'

	#Iniciando variáveis
	buff = BytesIO()
	arquivo = SimpleDocTemplate(buff, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=18)
	elements = []
	style = getSampleStyleSheet()
	style.add(ParagraphStyle(name='center', alignment=TA_CENTER))

	label = 'Números aleatórios'
	elements.append(Paragraph(label, style['title']))
	elements.append(Spacer(1, 24))

	#Explicação como usar
	label = """Esse documento deve ser impresso e
	recortado com o intuito de ser anexada para identificar a amostra.
	Também tem as "Chaves de controle", essas são usadas para o Provador
	ter acesso a página de resposta da análise,
	evitando fraudes na pesquisa."""


	elements.append(Paragraph(label, style['Normal']))
	elements.append(Spacer(1,10))

	label = """Para utilizar de maneira correta esse documento,
	recorte as plaquetas pela linha da tabela
	e cole no copinho que está a amostra. Esse número
	antes do número de amostra é o número do provador,
	ele deve ficar junto com os mesmo números iguais a ele.
	Por exemplo, em uma análise sensorial de 3 amostras
	deve ficar: 1-"AAA", 1-"BBB", 1-"CCC" e 1-"XXX" (chave de controle).
	Isso tudo irá compor um teste e terá que'
	ser disponibilizado para o provador."""

	elements.append(Paragraph(label, style['Normal']))
	elements.append(Spacer(1,24))

	for i in range(analise.quantidade_amostras):
		letra = str(transcricao_numero_letra(i))

		label = '<font size=17>Números da amostra "%s".</font>' % letra
		elements.append(Paragraph(label, style['center']))

		#Variáveis
		data = []
		line = []
		contador = 1

		for amostra in Amostra.objects.filter(analise_id=id, tipo=letra):
			line.append('%i-"%i"' % (contador, amostra.numero))

			#Ficará 6 números por linha
			if contador%6 == 0:
				data.append(line)
				line = []

			contador += 1

		#Quando a quantidade não for divisivel por 6,irá executar esse método
		if len(line) < 6 and len(line) != 0:
			falta = 6 - len(line)
			for quantidade in range(falta):
				line.append(None)
			data.append(line)

		elements.append(Spacer(1,24))
		table = Table(data, colWidths=95, rowHeights=50)
		table.setStyle(TableStyle([
	        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
	        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
			('FONTSIZE', (0,0), (-1,-1), 18),
			('TEXTFONT', (0,0), (-1, -1), "Times-Bold"),
			('ALIGN',(0,0),(-1,-1),'CENTER'),
			('VALIGN',(0,0),(-1,-1),'MIDDLE'),]))

		elements.append(table)
		elements.append(Spacer(1,24))
	#Renderizando documento
	arquivo.build(elements, canvasmaker=NumberedCanvas)
	response.write(buff.getvalue())
	buff.close()
	return response
