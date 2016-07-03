class confirmacao_cadastro(object):
#Classe utilizada para exibir a mensagem de confirmãção de cadastro do usuário
	def __init__(self):
		self.confirmacao = False
		self.constante = False
	def setConfirmacao(self, confirmacao):
		self.confirmacao = confirmacao

	def getConfirmacao(self):
		return self.confirmacao
