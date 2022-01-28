from abc import ABC, abstractmethod

class Variavel(ABC):
	def __init__(self, nome, endereco):
		self.nome = nome #lexema
		self.enderecoAlocacao = endereco


	def getNome(self):
		return self.nome
	def setNome(self, nome):
		self.nome = nome

	def getEnderecoAlocacao(self):
		return self.enderecoAlocacao

	def setEnderecoAlocacao(self, endereco):
		self.enderecoAlocacao = endereco



class Integer(Variavel):
	def __init__(self, nome, endereco, valor):
		super().__init__(nome, endereco)

		self.valor = valor


	def getValor(self):
		return self.valor

	def setValor(self, valor):
		self.valor = valor



class Boolean(Variavel):
	def __init__(self, nome, endereco, valor):
		super().__init__(nome, endereco)

		self.valor = valor


	def getValor(self):
		return self.valor

	def setValor(self, valor):
		self.valor = valor

class Float(Variavel):
	def __init__(self, nome, endereco, valor):
		super().__init__(nome, endereco)

		self.valor = float(valor)

	def getValor(self):
		return self.valor

	def setValor(self, valor):
		self.valor = valor