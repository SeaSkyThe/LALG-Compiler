class SymbolTable():
	def __init__(self):
		self.fields = []
		self.table = []

	def insert(self):
		pass 

	def remove(self):
		pass 

	def search(self):
		pass

	def modify(self):
		pass

	def print_table(self):
		pass


class x(SymbolTable):
	def __init__(self):
		self.fields = ["cadeia", 'token', 'categoria', 'tipo', 'valor', 'utilizada']
		self.table = [] 

	def insert(self, cadeia, token, utilizada, categoria=None, tipo=None, valor=None): #cadeia se refere à cadeia resgatada do codigo ('a', 1, fat)
															 				#token se refere ao tipo de token (id, real, OPSUB)
															 				#categoria se refere ao tipo de estrutura (variavel, procedure, loop)
															 				#tipo se refere ao tipo de variável (caso a categoria seja variavel)
															 				#valor se refere ao valor que aquela variavel representa
															 				# OBS: QUALQUER CAMPO PODE SER NULO

		temp_dict = dict((field, None) for field in self.fields)

		temp_dict['cadeia'] = cadeia
		temp_dict['token'] = token
		temp_dict['categoria'] = categoria
		temp_dict['tipo'] = tipo
		temp_dict['valor'] = valor
		temp_dict['utilizada'] = utilizada

		self.table.append(temp_dict)

		return temp_dict

	def search(self, cadeia):
		for element in self.table:
			if(element['cadeia'] == cadeia):
				return element
		
		print('O elemento pesquisado não existe na tabela (não foi declarado).\n')
		return None
				


	def remove(self, cadeia):
		for element in self.table:
			if(element['cadeia'] == cadeia):
				self.table.remove(element)
				return element
		
		print('O elemento o qual tentou-se remover da tabela não existe (não foi declarado).\n')
		return None
				

class VariableTable(SymbolTable):
	def __init__(self):
		self.fields = ["cadeia", 'tipo', 'valor', 'utilizada']
		self.table = [] 

	def insert(self, cadeia, tipo, utilizada, valor=None): #utilizada = True ou False

		temp_dict = dict((field, None) for field in self.fields)

		temp_dict['cadeia'] = cadeia
		temp_dict['tipo'] = tipo
		temp_dict['valor'] = valor
		temp_dict['utilizada'] = utilizada

		self.table.append(temp_dict)

		return temp_dict

	def search(self, cadeia):
		for element in self.table:
			if(element['cadeia'] == cadeia):
				return element
		
		print('O elemento pesquisado (',cadeia,') não existe na tabela (não foi declarado).\n')
		return None
				


	def remove(self, cadeia):
		for element in self.table:
			if(element['cadeia'] == cadeia):
				self.table.remove(element)
				return element
		
		print('O elemento o qual tentou-se remover da tabela (',cadeia,') não existe (não foi declarado).\n')
		return None

	def modify(self, cadeia, valor):
		variavel = self.search(cadeia)
		if(variavel != None):
			variavel['valor'] = valor
			return True
		return False

	def get_value(self, cadeia):
		variavel = self.search(cadeia)
		if(variavel != None):
			if(variavel['tipo'] == 'int'):
				return int(variavel['valor'])
			elif(variavel['tipo'] == 'real'):
				return float(variavel['valor'])
			elif(variavel['tipo'] == 'boolean'):
				if(variavel['valor'] == 'false'):
					return False
				elif(variavel['valor'] == 'true'):
					return True

		return None

	def print_table(self):
		for line in self.table:
			print(line, '\n')
