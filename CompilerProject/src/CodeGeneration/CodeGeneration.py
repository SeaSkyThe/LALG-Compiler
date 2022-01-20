from Syntactic.Errors import *

from CodeGeneration.Variavel import *

errors = Errors()

class CodeGenerator():
	_instance = None
	def __new__(self, textOutput=None):
		if (self._instance is None):
			self._instance = super().__new__(self)

		return self._instance

	def __init__(self):
		self.codeArea = [] #lista - area de codigo
		self.indexCode = 0 #indice para marcar posicao atual na area de codigo

		self.dataArea = [] #pilha - area de dados
		self.indexData = 0 #indice para marcar posical atual na pilha de dados

		self.contadorData = 0


		self.nomePrograma = ""

		self.listaVariaveis = {}
		self.listaComandos = []


		self.foiExecutado = None #booleano


		self.posicaoExpressao = None 
		self.posicaoIF = [] #pilha
		self.posicaoIF2 = [] #pilha
		self.posicaoELSE = [] #pilha
		self.posicaoWHILE = [] #pilha

	def getListaVariaveis(self):
		return self.listaVariaveis

	def getListaComandos(self):
		return self.listaComandos

	def getNomePrograma(self):
		return self.nomePrograma

	def setNomePrograma(self, nome):
		self.nomePrograma = nome


	def getContador(self):
		return len(self.listaComandos)

	#FUNCOES PARA GERAR OS CODIGOS

	def iniciarPrograma(self, nome):
		if(errors.has_errors()):
			return

		else:
			self.nomePrograma = nome
			self.listaComandos.append('INPP ')


	def declararVariavel(self, nomeVariavel, tipo): # fazer float
		if(errors.has_errors()):
			return


		variavel = ""

		if(tipo == 'int'):
			variavel = Integer(nomeVariavel, self.contadorData, None)
			self.contadorData = self.contadorData + 1

		elif(tipo == 'boolean'):
			variavel = Boolean(nomeVariavel, self.contadorData, None)
			self.contadorData = self.contadorData + 1

		self.listaVariaveis[nomeVariavel] = variavel
		self.listaComandos.append("AMEM 1")

	def atribuicaoVariavel(self, nomeVariavel, valor):
		if(errors.has_errors()):
			return

		self.listaVariaveis[nomeVariavel].setValor(valor)

		enderecoAlocacao = self.listaVariaveis[nomeVariavel].getEnderecoAlocacao()

		self.listaComandos.append("ARMZ " + str(enderecoAlocacao))


	def leituraInteiro(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("LEIT")

	def leituraCaracter(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("LEICH")

	def verificaIF(self):
		if(errors.has_errors()):
			return

		self.posicaoIF.append(len(self.listaComandos))

		self.executaNada()

	def desvioIF(self):
		if(errors.has_errors()):
			return

		self.desvioSeFalso(self.posicaoIF[-1], len(self.listaComandos))
		self.posicaoIF2.append(self.posicaoIF.pop())



	def verificaElse(self):
		if(errors.has_errors()):
			return

		executaNada()
		self.posicaoELSE.append(len(self.listaComandos) - 1)


	def setExpressao(self, num):
		if(errors.has_errors()):
			return

		self.posicaoExpressao = num;

	def desvioElse(self):
		if(errors.has_errors()):
			return

		self.desvioIncondicional(self.posicaoELSE[-1], len(self.listaComandos))
		self.desvioSeFalso(posicaoIF2.pop(), posicaoELSE.pop() + 1)


	def verificaWhile(self):
		if(errors.has_errors()):
			return

		self.posicaoWHILE.append(len(self.listaComandos))
		executaNada()


	def desvioWhile(self):
		if(errors.has_errors()):
			return

		executaNada()
		self.desvioIncondicional(len(self.listaComandos) - 1, self.posicaoExpressao)
		self.desvioSeFalso(posicaoWHILE.pop(), len(self.listaComandos))


	def desvioIncondicional(self, posicaoComando, posicaoDesvio):
		if(errors.has_errors()):
			return

		self.listaComandos[posicaoComando] = "DSVS " + str(posicaoDesvio)

	def desvioSeFalso(self, posicaoComando, posicaoDesvio):
		if(errors.has_errors()):
			return

		self.listaComandos[posicaoComando] = "DSVF " + str(posicaoDesvio)



	def verificaRelacao(self, operador):
		if(errors.has_errors()):
			return

		if(operador == "="):
			self.comparaIgual()
		elif(operador == "<"):
			self.comparaMenor()
		elif(operador == "<="):
			self.comparaMenorIgual()
		elif(operador == ">="):
			self.comparaMaior()
		elif(operador == ">"):
			self.comparaMaiorIgual()


	def comparaIgual(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CMIG")

	def comparaMenor(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CMME")

	def comparaMenorIgual(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CMEG")

	def comparaMaiorIgual(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CMAG")

	def comparaMaior(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CMMA")



	def inverterSinal(self):
		if(errors.has_errors()):
			return

		self.inversao()

	def inversao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("INVR")


	def verificarOperador(self, operador):
		if(errors.has_errors()):
			return

		if(operador == "+"):
			self.adicao()
		elif(operador == "-"):
			self.subtracao()
		elif(operador == "*"):
			self.multiplicacao()
		elif(operador == "/"):
			self.divisao()
		elif(operador == "div"):
			self.divisaoInteira()
		elif(operador == "or"):
			self.disjuncao()
		elif(operador == "and"):
			self.conjuncao()
		elif(operador == "not"):
			self.negacao()


	def adicao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("SOMA")

	def subtracao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("SUBT")

	def multiplicacao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("MULT")

	def divisao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("DIVI")

	def divisaoInteira(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("MODI")

	def disjuncao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("DISJ")

	def conjuncao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CONJ")

	def negacao(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("NEGA")


	def carregaValorConstante(self, valor):
		if(errors.has_errors()):
			return

		self.listaComandos.append("CRCT " + str(valor))

	def carregaValorDaVariavel(self, nomeVariavel):
		if(errors.has_errors()):
			return

		enderecoAlocacao = self.listaVariaveis[nomeVariavel].getEnderecoAlocacao()

		self.listaComandos.append("CRVL " + str(enderecoAlocacao))

	def executaNada(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("NADA")


	def imprimeInteiro(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("IMPR")

	def imprimeCaracter(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("IMPC")

	def imprimeNovaLinha(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("IMPE")

	def alocaMemoria(self, n):
		if(errors.has_errors()):
			return

		self.listaComandos.append("AMEM " + n)

	def desalocaMemoria(self, n):
		if(errors.has_errors()):
			return

		self.listaComandos.append("DMEM " + n)

	def finalizarPrograma(self):
		if(errors.has_errors()):
			return

		self.listaComandos.append("PARA")


	#READ E WRITE de lista de variaveis talvez seja necessario

	#

	def salvarEmArquivo(self, caminho):
		with open(caminho, 'w') as file:
			for comando in self.listaComandos:
				file.write("%s\n" % comando)

