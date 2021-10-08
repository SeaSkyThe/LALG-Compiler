import ply.lex as lex
import re

class MyLexer(object):
	def __init__(self, textOutput=None):
		self.textOutput = textOutput
		self.input = ""
		self.output = ""

		self.tokensExtenso = {
		'REAL': 'TIPO REAL',						#NUMERO REAL
		'INT': 'TIPO INTEIRO', 					#NUMERO INTEIRO
		'BOOLEAN': 'TIPO BOOLEANO',						#VALOR BOOLEANO
		'OPSOMA': 'OPERADOR SOMA',					#OPERADOR SOMA
		'OPSUB': 'OPERADOR SUBTRACAO', 				#OPERADOR SUBTRACAO
		'OPMUL': 'OPERADOR MULTIPLICACAO', 			#OPERADOR MULTIPLICACAO
		'OPDIV': 'OPERADOR DIVISAO', 				#OPERADOR DIVISAO
		'OPIGUAL_ATRIB': 'OPERADOR ATRIBUIÇÃO',		#OPERADOR DE IGUAL DE ATRIBUIÇÃO :=
		'OPIGUAL_COMP': 'OPERADOR COMPARAÇÃO',		#OPERADOR DE IGUAL DE COMPARAÇÃO =
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
		'FIM_LINHA': 'FINAL DA LINHA',
		'SEPARADOR': "SEPARADOR VIRGULA",
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
		}
	# DEFININDO PARAMETROS DO ANALISADOR LEXICO
	# listando os tokens
	tokens = (
		#'REAL',				#NUMERO REAL
		#'INT', 				#NUMERO INTEIRO
		'OPSOMA',				#OPERADOR SOMA
		'OPSUB', 				#OPERADOR SUBTRACAO
		'OPMUL', 				#OPERADOR MULTIPLICACAO
		'OPDIV', 				#OPERADOR DIVISAO
		'OPIGUAL_ATRIB',		#OPERADOR DE IGUAL DE ATRIBUIÇÃO :=
		'OPIGUAL_COMP',			#OPERADOR DE IGUAL DE COMPARAÇÃO =
		'MAIOR',
		'MENOR',
		'MAIOR_IGUAL',
		'MENOR_IGUAL',
		'FIM_LINHA',			#DELIMITADOR DE FIM DA LINHA ';'
		'SEPARADOR', 			#SEPARADOR ','
		'AP',    				#ABRE PARENTESES
		'FP',	 				#FECHA PARENTESES
		#'PROGRAM',				#PALAVRA QUE INICIA O PROGRAMA
		#'END', 					#PALAVRA QUE FINALIZA BLOCOS
		'ID',               	#IDENTIFICADOR
	) + tuple(reserved.values())

	# Specifying tokens as regex - AS: METACHARACTERS = . ^ $ * + ? { } [ ] \ | ( )
	# As a pattern of PLY, any regex has to be defined with the variable name of: 't_NOMEDOTOKEN'
	# Como padrão da biblioteca, as expressões regulares tem que ser definidas com nome de variavel = 't_NOMEDOTOKEN'
	t_OPSOMA = r'\+'
	t_OPSUB = r'-'
	t_OPMUL = r'\*'
	t_OPDIV = r'/'
	t_AP = r'\('
	t_FP = r'\)'

	t_OPIGUAL_ATRIB = r':='
	t_OPIGUAL_COMP = r'='
	t_MAIOR_IGUAL = r'>='
	t_MAIOR = r'>'
	t_MENOR_IGUAL = r'<='
	t_MENOR = r'<'

	t_FIM_LINHA = r';'
	t_SEPARADOR = r','

	# CARACTERES IGNORADOS - APENAS ESPACOS E TABULACOES
	t_ignore = ' \t:'

	# NUMEROS E IDENTIFICADORES

	def t_ID(self, t):
		r'[a-zA-Z_][a-zA-Z_0-9]*' 
		t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
		return t

	# Especificação em forma de função, pois no caso dos numeros é necessária uma conversão deles
	def t_REAL(self, t):
		r'(\d+\.\d+)'
		# r'[+-]?(\d+\.\d+)'
		t.value = float(t.value)
		return t

	def t_INT(self, t):
		# r'[+-]?\d+'
		r'\d+'
		t.value = int(t.value)
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
		self.lexer = lex.lex(module=self, **kwargs, debug=True)
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