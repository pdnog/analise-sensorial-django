# Create your views here.
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from random import randint
from io import StringIO 


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