class Errors(object):
	_instance = None
	def __new__(self, textOutput=None):
		if (self._instance is None):
			self._instance = super().__new__(self)

		return self._instance

	def __init__(self):
		self.ERROR_VARIAVEL_NAO_DECLARADA = "ERROR: variavel-nao-declarada"
		self.ERROR_TIPO = "ERROR: tipo"
		self.ERROR_VARIAVEL_JA_DECLARADA = "ERROR: variavel-ja-declarada"
		self.ERROR_VARIAVEL_SEM_VALOR = "ERROR: variavel-sem-valor"

		self.errorList = []

		self.WARNING_VARIAVEL_NAO_UTILIZADA = "WARNING: variavel-nao-utilizada"
		self.warningList = []


		self.ERROR_PROCEDURE_NAO_DECLARADA = "ERROR: procedure-nao-declarada"
		self.ERROR_PROCEDURE_JA_DECLARADA = "ERROR: procedure-ja-declarada"

		self.ERROR_READ_PARAMETROS = "ERROR: parametros-read-incoerentes"
		
		

	def add_error(self, error):
		self.errorList.append(error)
		return True

	def add_warning(self, warning):
		self.warningList.append(warning)
		return True

	def clear_errors(self):
		self.errorList = []
		return True

	def clear_warnings(self):
		self.warningList = []
		return True

	def get_errorList(self):
		return self.errorList

	def get_warningList(self):
		return self.warningList

	def has_errors(self):
		if(len(self.errorList) > 0):
			return True

		return False