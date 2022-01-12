from Syntactic.SymbolTable import *


class Scope():
	def __init__(self):
		print("\n\n=====NOVO ESCOPO CRIADO=====\n\n")
		self.procedureTable = ProcedureTable()
		self.variableTable = VariableTable()


