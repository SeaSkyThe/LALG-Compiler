from PyQt5 import QtCore, QtGui, QtWidgets

from Syntactic.Errors import *

from CodeGeneration.CodeGeneration import *

codeGenerator = CodeGenerator()

import time
errors = Errors()

readFile = 'ReadWrite-Files/read.txt'
writeFile = 'ReadWrite-Files/writeInterpreter.txt'

class Interpreter:
	_instance = None
	def __new__(self, textOutput=None):
		if (self._instance is None):
			self._instance = super().__new__(self)

		return self._instance

	def __init__(self):
		self.text = ""
		self.code = [] #lista
		self.stack = [] #pilha

		self.instructionCounter = 0;

		self.incrementFlag = True
		self.stopFlag = False


		#Contador de leitura 
		#self.leit_count = 0

		#Lista para ser printada 
		self.print_list = ""


		#Inicializando arquivo
		with open(writeFile, "w") as f:
			f.write("")


	def setStack(self, stack):
		self.stack = stack

	def getStack(self):
		return self.stack

	def setCode(self, code):
		self.code = code

	def getCode(self):
		return self.code

	def setText(self, text):
		self.text = text

	def getText(self):
		return self.text

	def setInstructionCounter(self, counter):
		self.instructionCounter = counter


	def readFile(self, path):
		##resetando configuracoes
		self.code = []
		self.text = ""
		with open(writeFile, "w") as f:
			f.write("")

		with open(path, "r") as file:
			self.code = file.read().splitlines()

		for instruction in self.code:
			self.code[self.code.index(instruction)] = list(instruction.split(" "))

		for linha in self.code:
			for parte in linha:
				self.text = self.text + parte + " "
			self.text = self.text + "\n"



	def execute(self, window):

		#self.revise()


		self.instructionCounter = 0;

		self.incrementFlag = True
		self.stopFlag = False

		#self.leit_count = 0

		self.print_list = ""

		command = None

		print("\n\n\nCODIGO: \n\n" + str(self.code))
		while(self.instructionCounter < len(self.code)):
			try:

				command = self.code[self.instructionCounter] #lista de comandos

				print(str(command) + " Contador: " + str(self.instructionCounter) + "\n")

				self.interpreta(command, window)

				print(str(self.stack) + "\n\n")

				if(self.incrementFlag):
					self.instructionCounter = self.instructionCounter + 1

				else:
					self.incrementFlag = True

				if(self.stopFlag):
					return self.print_list

			except Exception as e:
				print("ERROR: Execution Error: " + str(e))

		 

	def interpreta(self, command, window):
		#CASO FOR LER PELO ARQUIVO TIRAR COMENTARIO DAS LINHAS ABAIXO ATE A SEPARACAO

		# leit_list = None

		# with open(readFile, "r") as f:
		# 	leit_list = f.read().split(" ")

		#=============================================
		
		#print(command[0] + "\n")


		if(command[0] == "CRCT"): #CARREGA CONSTANTE
			self.stack.append(int(command[1]))

		elif(command[0] == "CRVL"): #CARREGA VALOR DE VARIAVEL
			self.stack.append(self.stack[int(command[1])])

		elif(command[0] == "ARMZ"): #ARMAZENA
			self.stack[int(command[1])] = self.stack.pop()

		elif(command[0] == "SOMA"):
			a = self.stack.pop()
			b = self.stack.pop()
			self.stack.append(b+a)

		elif(command[0] == "SUBT"):
			a = self.stack.pop()
			b = self.stack.pop()
			self.stack.append(b - a)

		elif(command[0] == "MULT"):
			a = self.stack.pop()
			b = self.stack.pop()
			self.stack.append(b*a)

		elif(command[0] == "DIVI"):
			a = self.stack.pop()
			b = self.stack.pop()

			try:
				self.stack.append(b/a)
			except ZeroDivisionError:
				errors.add_error("ERROR: Zero Division")
				self.stack.append(-100000)


		elif(command[0] == "MODI"): #DIVISAO INTEIRA
			a = self.stack.pop()
			b = self.stack.pop()
			
			self.stack.append(b//a)

		elif(command[0] == "CONJ"): #AND
			result = None

			a = self.stack.pop()
			b = self.stack.pop()
			
			if(a == 1 and b == 1):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "DISJ"): #OR
			result = None

			a = self.stack.pop()
			b = self.stack.pop()
			
			if(a == 1 or b == 1):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "INVR"): #NOT
			a = self.stack.pop()
			self.stack.append(-a)

		elif(command[0] == "NEGA"):
			result = None

			a = self.stack.pop()
			
			self.stack.append(1 - a)
			
		elif(command[0] == "CMME"): #COMPARA SE MENOR
			a = self.stack.pop()
			b = self.stack.pop()

			if(b < a):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "CMEG"):#COMPARA SE MENOR OU IGUAL
			a = self.stack.pop()
			b = self.stack.pop()

			if(b <= a):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "CMMA"): #COMPARA SE MAIOR
			a = self.stack.pop()
			b = self.stack.pop()

			if(b > a):
				self.stack.append(1)
			else:
				self.stack.append(0)

		
		elif(command[0] == "CMAG"): #COMPARA SE MAIOR OU IGUAL
			a = self.stack.pop()
			b = self.stack.pop()

			if(b >= a):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "CMIG"): #COMPARA SE IGUAL

			a = self.stack.pop()
			b = self.stack.pop()

			if(b == a):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "CMDG"): #COMPARA SE DESIGUAL
			a = self.stack.pop()
			b = self.stack.pop()

			if(b != a):
				self.stack.append(1)
			else:
				self.stack.append(0)

		elif(command[0] == "DSVS"): #DESVIO INCONDICIONAL
			self.instructionCounter = int(command[1])
			self.incrementFlag = False

		elif(command[0] == "DSVF"): #DESVIO VERDADEIRO FALSO
			a = self.stack.pop()

			if(a == 0):
				self.instructionCounter = int(command[1])
				self.incrementFlag = False

		elif(command[0] == "NADA"): #faz nada
			pass

		elif(command[0] == "LEIT"): # LEITURA DE INTEIRO - TALVEZ COLOCAR UMA JANELA PARA INTRODUZIR VALOR - POR ENQUANTO FAZEMOS PELO ARQUIVO
			number, confirmed = QtWidgets.QInputDialog.getInt(window, 'Input', 'Digite um inteiro: ')
			self.stack.append(number)

			# a = int(leit_list[self.leit_count])
			# self.leit_count = self.leit_count + 1

			# self.stack.append(a)

		elif(command[0] == "LEICH"): # LEITURA DE CHAR - TALVEZ COLOCAR UMA JANELA PARA INTRODUZIR VALOR - POR ENQUANTO FAZEMOS PELO ARQUIVO
			character, confirmed = QtWidgets.QInputDialog.getInt(window, 'Input', 'Digite um char: ')
			self.stack.append(chr(character))

			# a = chr(leit_list[self.leit_count])
			# self.leit_count = self.leit_count + 1

			# self.stack.append(a)

		elif(command[0] == "IMPR"):
			a = int(self.stack.pop())

			#imprimindo no arquivo
			with open(writeFile, "a") as f:
				f.write(str(a) + " ")

			#guardando para ser impresso na tela
			self.print_list = self.print_list + str(a) + "\n"
			

		elif(command[0] == "IMPC"):
			a = chr(self.stack.pop())

			with open(writeFile, "a") as f:
				f.write(a + " ")

		elif(command[0] == "IMPE"):
			with open(writeFile, "a") as f:
				f.write("\n")

		elif(command[0] == "INPP"):
			self.instructionCounter = 0
			self.stack = []

		elif(command[0] == "AMEM"):
			for i in range(0, int(command[1])):
				self.stack.append(0)
			pass

		elif(command[0] == "DMEM"):
			for i in range(0, int(command[1])):
				self.stack.pop()
			pass

		elif(command[0] == "PARA"):
			self.stopFlag = True


	#FUNCOES DE REVISAO CASO SEJA NECESSARIO REVISAR O CODIGO PRE INTERPRETACAO

	# def revise(self):
	# 	for command in self.code:
	# 		self.verifyConstValueOrder(command)

	# def verifyConstValueOrder(self, command): #funcao para corrigir o bug de ordem para operacoes com constante à esquerda ex: b/4
		

	# 	code_list_with_details = codeGenerator.getListaComandos() #essa lista é -1 em relação a lista presente no interpretador, entao qualquer
	# 															  #uso de index tem que ser adicionado o -1

	# 	operations_that_order_matters = ["DIVI", "MODI","CMME","CMEG","CMMA","CMAG","CMIG","CMDG"]

	# 	if(command[0] in operations_that_order_matters):
	# 		command_index = self.code.index(command)

	# 		if(self.code[command_index - 1][0] == "CRVL" and self.code[command_index - 2][0] == "CRCT"): #se for um Carrega constante seguido de um carrega variavel
	# 			if(code_list_with_details[command_index - 2][2] < code_list_with_details[command_index - 3][2]): #e se a variavel vem antes da constante
	# 																								#temos que inverter a ordem desses comandos
	# 				self.code[command_index - 1], self.code[command_index - 2] = self.code[command_index - 2], self.code[command_index - 1]


		


	
	 