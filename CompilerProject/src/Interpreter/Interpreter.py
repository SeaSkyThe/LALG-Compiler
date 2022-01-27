from Syntactic.Errors import *
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

		self.leit_count = 0

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


	def execute(self):

		self.instructionCounter = 0;

		self.incrementFlag = True
		self.stopFlag = False

		self.leit_count = 0

		command = None


		while(self.instructionCounter < len(self.code)):
			try:
				command = self.code[self.instructionCounter] #lista de comandos
				
				with open("ERRORLOG-INTERPRETER.txt", "a") as f:
					f.write(str(command) + " Contador: " + str(self.instructionCounter) + "\n")

				print(str(command) + " Contador: " + str(self.instructionCounter) + "\n")
				self.interpreta(command)
				print(str(self.stack) + "\n\n")

				with open("ERRORLOG-INTERPRETER.txt", "a") as f:
					f.write(str(self.stack) + "\n\n")


				if(self.incrementFlag):
					self.instructionCounter = self.instructionCounter + 1

				else:
					self.incrementFlag = True

				if(self.stopFlag):
					return

				

			except Exception as e:
				with open("ERRORLOG-INTERPRETER.txt", "a") as f:
					f.write(str(e))
				print("ERROR: Execution Error: " + str(e))


	def interpreta(self, command):
		leit_list = None

		with open(readFile, "r") as f:
			leit_list = f.read().split(" ")

		
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
				errors.add_error("ERROR: Zero Division Error ")
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
			a = int(leit_list[self.leit_count])
			self.leit_count = self.leit_count + 1

			self.stack.append(a)

		elif(command[0] == "LEICH"): # LEITURA DE INTEIRO - TALVEZ COLOCAR UMA JANELA PARA INTRODUZIR VALOR - POR ENQUANTO FAZEMOS PELO ARQUIVO
			a = chr(leit_list[self.leit_count])
			self.leit_count = self.leit_count + 1

			self.stack.append(a)

		elif(command[0] == "IMPR"):
			a = int(self.stack.pop())

			with open(writeFile, "a") as f:
				f.write(str(a) + " ")

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