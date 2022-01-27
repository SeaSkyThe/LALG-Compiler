import ply.lex as lex
import re

#implementando com Singleton
class myLexer(object):
	_instance = None

	def __new__(self, textOutput=None):
		if (self._instance is None):
			self._instance = super().__new__(self)
		return self._instance

	def __init__(self, textOutput=None):
		self.textOutput = textOutput
		self.input = ""
		self.output = ""
		self.lexer = None

		self.tokensExtenso = {
		'REAL': 'TIPO REAL',						#TIPO REAL
		'INT': 'TIPO INTEIRO', 						#TIPO INTEIRO
		'BOOLEAN': 'TIPO BOOLEANO',						#VALOR BOOLEANO
		'NUM_REAL': 'NUMERO REAL',
		'NUM_INT': 'NUMERO INTEIRO',
		'OPSOMA': 'OPERADOR SOMA',					#OPERADOR SOMA
		'OPSUB': 'OPERADOR SUBTRACAO', 				#OPERADOR SUBTRACAO
		'OPMUL': 'OPERADOR MULTIPLICACAO', 			#OPERADOR MULTIPLICACAO
		'OPDIV': 'OPERADOR DIVISAO', 				#OPERADOR DIVISAO
		'OPIGUAL_ATRIB': 'OPERADOR ATRIBUIÇÃO',		#OPERADOR DE IGUAL DE ATRIBUIÇÃO :=
		'IGUAL': 'OPERADOR COMPARAÇÃO',		#OPERADOR DE IGUAL DE COMPARAÇÃO =
		'DESIGUAL': 'OPERADOR DIFERENTE',
		'MAIOR': 'OPERADOR MAIOR',
		'MENOR': 'OPERADOR MENOR',
		'MAIOR_IGUAL': 'OPERADOR MAIOR OU IGUAL',
		'MENOR_IGUAL': 'OPERADOR MENOR OU IGUAL',
		'AP': 'ABRE PARENTESES',    				#ABRE PARENTESES
		'FP': 'FECHA PARENTESES',	 				#FECHA PARENTESES
		'ID': 'IDENTIFICADOR', 						#IDENTIFICADOR
		'PROGRAM': 'INICIO DO PROGRAMA',			#INICIO DO PROGRAMA
		'BEGIN': 'INICIO DO BLOCO',					#INICIO DO BLOCO DE CODIGO
		'END': 'FIM DO BLOCO',						#FIM DO BLOCO
		'PROCEDURE': 'DECLARANDO PROCEDIMENTO',		#DECLARANDO PROCEDURE
		'VAR': 'DECLARANDO VARIAVEL', 
		'READ': 'COMANDO DE ENTRADA',
		'WRITE': 'COMANDO DE SAIDA', 
		'TRUE': 'VALOR BOOLEANO VERDADEIRO',
		'FALSE': 'VALOR BOOLEANO FALSE', 
		'IF': "COMANDO 'SE'",
		'THEN': "COMANDO 'ENTAO'",
		'ELSE': "COMANDO 'SE NAO'",
		'WHILE': "COMANDO 'ENQUANTO'",
		'DO': "COMANDO 'FAÇA'",
		'DIV': "FUNÇAO DIVISAO",
		'AND': "OPERADOR LÓGICO 'E'",
		'OR': "OPERADOR LÓGICO 'OU'",
		'NOT': "OPERADOR LÓGICO 'NAO'",
		'FIM_LINHA': 'FINAL DA LINHA',
		'SEPARADOR': "SEPARADOR VIRGULA",
		'PONTO_FINAL': 'PONTO FINAL',
		'DOIS_PONTOS': 'DOIS PONTOS',
		}

		
		# reserved words - to check if IDENTIFIERS are reserved or not
		self.reserved = {
			'program': 'PROGRAM',
			'begin': 'BEGIN',
			'end': 'END',
			'int': 'INT',
			'real': 'REAL',
			'boolean': 'BOOLEAN',
			'procedure': 'PROCEDURE',
			'var': 'VAR',
			'read': 'READ',
			'write': 'WRITE',
			'true': 'TRUE',
			'false': 'FALSE',
			'if': 'IF',
			'then': 'THEN',
			'else': 'ELSE',
			'while': 'WHILE',
			'do': 'DO',
			'div': 'DIV', #divisao
			'and': 'AND',
			'or': 'OR',
			'not': 'NOT',
		}
	#redeclaring
	reserved = {
			'program': 'PROGRAM',
			'begin': 'BEGIN',
			'end': 'END',
			'int': 'INT',
			'real': 'REAL',
			'boolean': 'BOOLEAN',
			'procedure': 'PROCEDURE',
			'var': 'VAR',
			'read': 'READ',
			'write': 'WRITE',
			'true': 'TRUE',
			'false': 'FALSE',
			'if': 'IF',
			'then': 'THEN',
			'else': 'ELSE',
			'while': 'WHILE',
			'do': 'DO',
			'div': 'DIV', #divisao
			'and': 'AND',
			'or': 'OR',
			'not': 'NOT',
		}
	# DEFININDO PARAMETROS DO ANALISADOR LEXICO
	# listando os tokens
	tokens = [
		'NUM_REAL',					#NUMERO REAL
		'NUM_INT', 					#NUMERO INTEIRO
		'OPSOMA',				#OPERADOR SOMA
		'OPSUB', 				#OPERADOR SUBTRACAO
		'OPMUL', 				#OPERADOR MULTIPLICACAO
		'OPDIV', 				#OPERADOR DIVISAO
		'OPIGUAL_ATRIB',		#OPERADOR DE IGUAL DE ATRIBUIÇÃO :=
		'IGUAL',				#OPERADOR DE IGUAL DE COMPARAÇÃO =
		'DESIGUAL',
		'MAIOR',
		'MENOR',
		'MAIOR_IGUAL',
		'MENOR_IGUAL',
		'FIM_LINHA',			#DELIMITADOR DE FIM DA LINHA ';'
		'SEPARADOR', 			#SEPARADOR ','
		'PONTO_FINAL', 			#DELIMITA FIM DO PROGRAMA '.'
		'DOIS_PONTOS',			#":"
		'AP',    				#ABRE PARENTESES
		'FP',	 				#FECHA PARENTESES
		#'PROGRAM',				#PALAVRA QUE INICIA O PROGRAMA
		#'END', 					#PALAVRA QUE FINALIZA BLOCOS
		'ID',               	#IDENTIFICADOR
	] + list(reserved.values())

	# Specifying tokens as regex - AS: METACHARACTERS = . ^ $ * + ? { } [ ] \ | ( )
	# As a pattern of PLY, any regex has to be defined with the variable name of: 't_NOMEDOTOKEN'
	# Como padrão da biblioteca, as expressões regulares tem que ser definidas com nome de variavel = 't_NOMEDOTOKEN'
	t_OPSOMA = r'\+'
	t_OPSUB = r'-'
	t_OPMUL = r'\*'
	t_OPDIV = r'/'
	t_AP = r'[(]'
	t_FP = r'[)]'

	t_OPIGUAL_ATRIB = r':='
	t_DOIS_PONTOS = r':'
	t_IGUAL = r'='
	t_DESIGUAL = r'<>'
	t_MAIOR_IGUAL = r'>='
	t_MAIOR = r'>'
	t_MENOR_IGUAL = r'<='
	t_MENOR = r'<'

	t_FIM_LINHA = r';'
	t_SEPARADOR = r','
	t_PONTO_FINAL = r'[.]'

	# CARACTERES IGNORADOS - APENAS ESPACOS E TABULACOES
	t_ignore = ' \t'

	# RESERVADAS

	#t_PROCEDURE = r'\bprocedure\b'
	# t_INT = r'\bint\b'
	# t_REAL = r'\breal\b'
	# t_BOOLEAN = r'\bboolean\b'


	def getTokens(self):
		return self.tokens
	# NUMEROS E IDENTIFICADORES

	def t_ID(self, t):
		#r'[a-zA-Z_][a-zA-Z_0-9]*' #*  = 0 ou more
		r'[a-zA-Z_][a-zA-Z_0-9]{0,50}' #definindo limite de caracteres
		t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
		return t

	# Especificação em forma de função, pois no caso dos numeros é necessária uma conversão deles
	def t_NUM_REAL(self, t):
		# r'(\d{40}\\.\d{40})' #40 casas decimais
		r'[+-]?(\d+\.\d+)'
		t.value = float(t.value)
		return t

	def t_NUM_INT(self, t):
		# r'[+-]?\d+'
		#r'\d+' # 1 ou mais
		r'\d{1,40}' #1 ate 40 digitos
		try:
			t.value = int(t.value)
		except:
			print("Valor do inteiro muito grande: ", t.value)
			t.value = 0
		return t



	# CONTAGEM DE LINHAS E COLUNAS

	# Contagem do numero de linhas, cada vez que aparecer uma quebra de linha, incrementamos o numero de linhas
	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)
		# depois de atualizar o numero da linha, damos um '\n' no output para separar por linhas
		self.output = self.output + "\nLINHA %d: \n" % t.lexer.lineno
		
	# Compute column.
	# input is the input text string
	# token is a token instance
	def find_column(self, token):
		line_start = self.input.rfind('\n', 0, token.lexpos) + 1
		return (token.lexpos - line_start) + 1

	# Comentarios
	def t_COMMENT(self, t):
		r'//.*|{[\s\S]*}'
		pass

	# Error handling
	def t_error(self, t):
		#caso seja diferente de um comentario
		if(t.value != '{'):
			self.output = self.output + "Caracter invalido '%s'" % t.value[0] + " - Linha %d " % t.lineno + " - Coluna %d \n" % self.find_column(t)
		
		#se for erro de comentario nao fechado
		elif(t.value == '{'):
			self.output = self.output + "Comentario iniciado e não finalizado - Linha %d " % t.lineno + " - Coluna %d \n" % self.find_column(t)
		
		#print(self.output)
		if(self.textOutput != None):
			self.textOutput.setText(self.output)
		t.lexer.skip(1)

	# Criando o analisador lexico
	def build(self, **kwargs):
		if(self.lexer == None):
			self.lexer = lex.lex(module=self, **kwargs, debug=False)
		return self.lexer

	# usando analisador lexico
	def use(self, text):
		self.output = "LINHA 1: \n"
		self.input = text
		self.lexer.input(text)
		for token in self.lexer:
			if not token:
				break
			self.output = self.output + str(token.value) + " => " + str(self.tokensExtenso[token.type]) +"\n"
		#print(self.output)

		if(self.textOutput != None):
			self.textOutput.setText(self.output)
		self.output = ""
		#print("\n")

#----------------------------------------------------------------------------------------------------------
		
# if __name__ == '__main__':
# 	lexer = MyLexer()
# 	lexer.build()
# 	lexer.use(input('Digite sua expressão aqui: '))

# 	#atributos de cada token: type, value, lineno(numero da linha), lexpos(posição na linha)
# 	# print("\n")
# 	# for token in lexer: 
# 	# 	print(token.value, " => ", tokens_extenso[token.type],'\n')
# 	# print("\n")
