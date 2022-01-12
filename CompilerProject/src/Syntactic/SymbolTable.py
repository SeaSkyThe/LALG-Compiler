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

				

class VariableTable(SymbolTable):
	def __init__(self):
		self.fields = ["lexema", 'tipo', 'valor', 'utilizada']
		self.token = 'id'
		self.table = [] 

	def insert(self, lexema, tipo, utilizada, valor=None): #utilizada = True ou False

		if(self.search(lexema) == None):
			temp_dict = dict((field, None) for field in self.fields)

			temp_dict['lexema'] = lexema
			temp_dict['tipo'] = tipo
			temp_dict['valor'] = valor
			temp_dict['utilizada'] = utilizada

			self.table.append(temp_dict)

			return temp_dict
		else:
			print('A variável ',lexema,' já foi declarada.\n')
			return None


	def search(self, lexema):
		for element in self.table:
			if(element['lexema'] == lexema):
				return element
		
		print('A variável pesquisada (',lexema,') não existe na tabela (não foi declarada).\n')
		return None
				


	def remove(self, lexema):
		for element in self.table:
			if(element['lexema'] == lexema):
				self.table.remove(element)
				return element
		
		print('A variável a qual tentou-se remover da tabela (',lexema,') não existe (não foi declarada).\n')
		return None

	def modify(self, lexema, valor):
		variavel = self.search(lexema)
		
		if((variavel['tipo'] == 'real' and isinstance(valor, float)) or (variavel['tipo'] == 'int' and isinstance(valor, int)) or (variavel['tipo'] == 'boolean' and isinstance(valor, bool))):
			variavel['valor'] = valor
			variavel['usada'] = True
			return variavel
		else:
			return "ERROR: tipo"

		return None

	def get_value(self, lexema):
		variavel = self.search(lexema)
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


class ProcedureTable(SymbolTable):
	def __init__(self):
		self.fields = ["lexema", 'parametros','variaveis_locais']
		self.token = "procedure"
		self.table = [] 
		self.tabelaParametros = VariableTable()
		self.tabelaVariaveisLocais = VariableTable()

	def insert(self, lexema, parametros, variaveis_locais=None): #lexema se refere à lexema resgatada do codigo ('a', 1, fat)
															 				#token se refere ao tipo de token (id, real, OPSUB)
															 				#categoria se refere ao tipo de estrutura (variavel, procedure, loop)
															 				#tipo se refere ao tipo de variável (caso a categoria seja variavel)
															 				#valor se refere ao valor que aquela variavel representa
															 				# OBS: QUALQUER CAMPO PODE SER NULO

		if(self.search(lexema) == None):
			

			temp_dict = dict((field, None) for field in self.fields)

			temp_dict['lexema'] = lexema

			for parametro in parametros:
				self.tabelaParametros.insert(parametro[1], parametro[0], None, None)

			temp_dict['parametros'] = self.tabelaParametros

			if(variaveis_locais != None):
				for variavelLocal in variaveis_locais:
					for variavel in variavelLocal[1]:
						self.tabelaVariaveisLocais.insert(variavel, variavelLocal[0], False, None)

				temp_dict['variaveis_locais'] = self.tabelaVariaveisLocais

			else:
				temp_dict['variaveis_locais'] = None

			self.table.append(temp_dict)

			return temp_dict

		else:
			print('A procedure ',lexema,' já foi declarada.\n')
			return None

	def search(self, lexema):
		for element in self.table:
			if(element['lexema'] == lexema):
				return element
		
		print('A procedure pesquisada (',lexema,') não existe na tabela (não foi declarada).\n')
		return None
				


	def remove(self, lexema):
		for element in self.table:
			if(element['lexema'] == lexema):
				self.table.remove(element)
				return element
		
		print('A procedure a qual tentou-se remover da tabela (',lexema,') não existe (não foi declarada).\n')
		return None

	def print_table(self):
		for line in self.table:
			for key in line:
				if(isinstance(line[key], VariableTable)):
					line[key].print_table()
				else:
					print(line[key])