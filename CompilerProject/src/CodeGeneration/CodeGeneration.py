from Syntactic.Errors import *

from CodeGeneration.Variavel import *


errors = Errors()


import inspect

DEBUG = False


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

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		else:
			self.nomePrograma = nome
			self.listaComandos.append('INPP')


	def declararVariavel(self, nomeVariavel, tipo): # fazer float
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()


		variavel = ""

		if(tipo == 'int'):
			variavel = Integer(nomeVariavel, self.contadorData, None)
			self.contadorData = self.contadorData + 1

			self.listaVariaveis[nomeVariavel] = variavel
			self.listaComandos.append("AMEM 1")

		elif(tipo == 'boolean'):
			variavel = Boolean(nomeVariavel, self.contadorData, None)
			self.contadorData = self.contadorData + 1

			self.listaVariaveis[nomeVariavel] = variavel
			self.listaComandos.append("AMEM 1")

		elif(tipo == 'real'):
			variavel = Float(nomeVariavel, self.contadorData, None)
			self.contadorData = self.contadorData + 1

			self.listaVariaveis[nomeVariavel] = variavel
			self.listaComandos.append("AMEM 1")
		
		else:
			erros.add_error("ERROR: Tipo nao existe\n")

	def atribuicaoVariavel(self, nomeVariavel, valor=None): #VERIFICAR SOBRE O VALOR DA VARIAVEL
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaVariaveis[nomeVariavel].setValor(valor)

		enderecoAlocacao = self.listaVariaveis[nomeVariavel].getEnderecoAlocacao()

		self.listaComandos.append("ARMZ " + str(enderecoAlocacao))


	def leituraInteiro(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("LEIT")

	def leituraCaracter(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("LEICH")

	def verificaIF(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.posicaoIF.append(len(self.listaComandos))
		self.executaNada()


	def desvioIF(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.desvioSeFalso(self.posicaoIF[0], len(self.listaComandos) + 1)
		self.posicaoIF2.append(self.posicaoIF.pop())


	def verificaElse(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()
			

		
		self.posicaoELSE.append(len(self.listaComandos))
		self.executaNada()

	def setExpressao(self, num):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.posicaoExpressao = num;


	def desvioElse(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

			

		posIF2 = self.posicaoIF2.pop()
		posELSE = self.posicaoELSE.pop()

		self.desvioIncondicional(posELSE, len(self.listaComandos) + 1)
		
		self.desvioSeFalso(posIF2, posELSE + 2)
		

	def verificaWhile(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.posicaoWHILE.append(len(self.listaComandos))
		self.executaNada()


	def desvioWhile(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		

		posWHILE = self.posicaoWHILE.pop()

		self.executaNada()
		self.desvioIncondicional(len(self.listaComandos) - 1, self.posicaoExpressao + 1)
		

		self.desvioSeFalso(posWHILE, len(self.listaComandos) + 1)


	def desvioIncondicional(self, posicaoComando, posicaoDesvio):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos[posicaoComando] = "DSVS " + str(posicaoDesvio)

	def desvioSeFalso(self, posicaoComando, posicaoDesvio):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos[posicaoComando] = "DSVF " + str(posicaoDesvio)



	def verificaRelacao(self, operador):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		if(operador == "="):
			self.comparaIgual()
		elif(operador == "<"):
			self.comparaMenor()
		elif(operador == "<="):
			self.comparaMenorIgual()
		elif(operador == ">="):
			self.comparaMaiorIgual()
		elif(operador == ">"):
			self.comparaMaior()
		elif(operador == "<>"):
			self.comparaDesigual()


	def comaparaDesigual(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CMDG")

	def comparaIgual(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CMIG")

	def comparaMenor(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CMME")

	def comparaMenorIgual(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CMEG")

	def comparaMaiorIgual(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CMAG")

	def comparaMaior(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CMMA")



	def inverterSinal(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.inversao()

	def inversao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("INVR")


	def verificaOperador(self, operador):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

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

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("SOMA")

	def subtracao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("SUBT")

	def multiplicacao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("MULT")

	def divisao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("DIVI")

	def divisaoInteira(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("MODI")

	def disjuncao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("DISJ")

	def conjuncao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CONJ")

	def negacao(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("NEGA")


	def carregaValorConstante(self, valor, posNaExpressao):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("CRCT " + str(valor) + " " + str(posNaExpressao))

	def carregaValorDaVariavel(self, nomeVariavel, posNaExpressao):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		try:
			enderecoAlocacao = self.listaVariaveis[nomeVariavel].getEnderecoAlocacao()

			self.listaComandos.append("CRVL " + str(enderecoAlocacao) + " " + str(posNaExpressao))
		except Exception as e:
			return e

	def executaNada(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("NADA")


	def imprimeInteiro(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("IMPR")

	def imprimeCaracter(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("IMPC")

	def imprimeNovaLinha(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("IMPE")

	def alocaMemoria(self, n):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("AMEM " + n)

	def desalocaMemoria(self, n):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("DMEM " + n)

	def finalizarPrograma(self):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		self.listaComandos.append("PARA")


	#READ E WRITE de lista de variaveis talvez seja necessario

	def listaVariaveisRead(self, lista_de_variaveis):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		for variavel in lista_de_variaveis:
			self.leituraInteiro()
			self.atribuicaoVariavel(variavel)


	def listaVariaveisWrite(self, lista_de_variaveis, posNaExpressao):
		if(errors.has_errors()):
			return

		if(DEBUG):
			print(str(inspect.stack()[0][3]) + ": ")
			self.printComandos()

		for variavel in lista_de_variaveis:
			self.carregaValorDaVariavel(variavel, posNaExpressao)
			self.imprimeInteiro()

	#

	def salvarEmArquivo(self, caminho):
		self.revise()

		count = 0

		with open(caminho, 'w') as file:
			file.write("{comand}\n".format(comand='INPP'))
			print("0: INPP\n")
			count = count + 1
			for comando in self.listaComandos:
				print(str(count) + ": ", end="")
				if(len(comando) >= 2):
					file.write("{comand} {argument}\n".format(comand=comando[0], argument=comando[1]))
					print(str(comando[0]) + " " +str(comando[1]) + "\n")
				else:
					file.write("{comand}\n".format(comand=comando[0]))
					print(str(comando[0]) + "\n")

				count = count + 1

	def revise(self):
		for comando in self.listaComandos:
			self.listaComandos[self.listaComandos.index(comando)] = list(comando.split(" "))

		for comando in self.listaComandos:
			self.verifyConstValueOrder(comando)

	def verifyConstValueOrder(self, command): #funcao para corrigir o bug de ordem para operacoes com constante à esquerda ex: b/4
		
		print("\n\nEntrou na verificação com o comando: " + str(command))

		operations_that_order_matters = ["DIVI", "MODI","CMME","CMEG","CMMA","CMAG","CMIG","CMDG"]

		if(command[0] in operations_that_order_matters):
			command_index = self.listaComandos.index(command)

			#print("\n\nComandos antes: " + str(self.code[command_index - 1]) + str(self.code[command_index - 2]))

			if(self.listaComandos[command_index - 1][0] == "CRVL" and self.listaComandos[command_index - 2][0] == "CRCT"): #se for um Carrega constante seguido de um carrega variavel
				print("\n\nComandos na lista detalhada: " + str(self.listaComandos[command_index - 1][2]) +" "+ str(self.listaComandos[command_index - 2][2]))
				if(self.listaComandos[command_index - 1][2] < self.listaComandos[command_index - 2][2]): #e se a variavel vem antes da constante
																									#temos que inverter a ordem desses comandos
					self.listaComandos[command_index - 1], self.listaComandos[command_index - 2] = self.listaComandos[command_index - 2], self.listaComandos[command_index - 1]


					print("\n\nModificou com o comando: " + str(command))
					print("\n\nLista pos modificada: " + str(self.listaComandos))

	def printComandos(self):
		print(self.listaComandos)
		print("\n")