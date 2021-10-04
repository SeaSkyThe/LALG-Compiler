import ply.lex as lex
import re

class MyLexer(object):
	def __init__(self, textOutput=None):
		self.textOutput = textOutput
		self.tokensExtenso = {
		'FLOAT': 'NUMERO REAL',				#NUMERO REAL
		'INT': 'NUMERO INTEIRO', 			#NUMERO INTEIRO
		'OPSOMA': 'OPERADOR SOMA',			#OPERADOR SOMA
		'OPSUB': 'OPERADOR SUBTRACAO', 		#OPERADOR SUBTRACAO
		'OPMUL': 'OPERADOR MULTIPLICACAO', 	#OPERADOR MULTIPLICACAO
		'OPDIV': 'OPERADOR DIVISAO', 		#OPERADOR DIVISAO
		'AP': 'ABRE PARENTESES',    		#ABRE PARENTESES
		'FP': 'FECHA PARENTESES',	 		#FECHA PARENTESES
		}

		self.output = ""
	# DEFININDO PARAMETROS DO ANALISADOR LEXICO
	# listando os tokens
	tokens = (
		'FLOAT',	#NUMERO REAL
		'INT', 		#NUMERO INTEIRO
		'OPSOMA',	#OPERADOR SOMA
		'OPSUB', 	#OPERADOR SUBTRACAO
		'OPMUL', 	#OPERADOR MULTIPLICACAO
		'OPDIV', 	#OPERADOR DIVISAO
		'AP',    	#ABRE PARENTESES
		'FP',	 	#FECHA PARENTESES
	)

	# Especificando os tokens com expressões regulares - ANOTACAO: METACHARACTERS = . ^ $ * + ? { } [ ] \ | ( )
	# Como padrão da biblioteca, as expressões regulares tem que ser definidas com nome de variavel = 't_NOMEDOTOKEN'
	t_OPSOMA = r'\+'
	t_OPSUB = r'-'
	t_OPMUL = r'\*'
	t_OPDIV = r'/'
	t_AP = r'\('
	t_FP = r'\)'


	# NUMEROS E IDENTIFICADORES

	# Especificação em forma de função, pois no caso dos numeros é necessária uma conversão deles
	def t_FLOAT(self, t):
		r'(\d+\.\d+)'
		# r'[+-]?(\d+\.\d+)'
		t.value = float(t.value)
		return t

	def t_INT(self, t):
		# r'[+-]?\d+'
		r'\d+'
		t.value = int(t.value)
		return t




	
	# Contagem do numero de linhas, cada vez que aparecer uma quebra de linha, incrementamos o numero de linhas
	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	# Tabulação e espaços serão ignorados
	t_ignore = ' \t'

	# Comentarios
	def t_COMMENT(self, t):
		r'//.*|{[\s\S]*}'
		pass

	# Error handling
	def t_error(self, t):
		self.output = self.output + "Caracter invalido '%s' \n" % t.value[0]
		
		print(self.output)
		if(self.textOutput != None):
			print("OUTPUT ACESSADO\n")
			self.textOutput.setText(self.output)
		t.lexer.skip(1)

	# Criando o analisador lexico
	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)
		return self.lexer

	# usando analisador lexico
	def use(self, text):
		self.lexer.input(text)
		for token in self.lexer:
			if not token:
				break
			self.output = self.output + str(token.value) + " => " + str(self.tokensExtenso[token.type]) +"\n"
			print(self.output)

		if(self.textOutput != None):
			self.textOutput.setText(self.output)

		print("\n")

----------------------------------------------------------------------------------------------------------
		
if __name__ == '__main__':
	lexer = MyLexer()
	lexer.build()
	lexer.use(input('Digite sua expressão aqui: '))

	#atributos de cada token: type, value, lineno(numero da linha), lexpos(posição na linha)
	# print("\n")
	# for token in lexer: 
	# 	print(token.value, " => ", tokens_extenso[token.type],'\n')
	# print("\n")