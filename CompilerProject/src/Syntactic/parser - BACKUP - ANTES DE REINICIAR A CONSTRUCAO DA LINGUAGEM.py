#TODO, DECLARACAO DE VARIAVEIS

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from Lexic.LALGLex import myLexer


readFile = 'ReadWrite-Files/read.txt'
writeFile = 'ReadWrite-Files/write.txt'

# FUNÇÕES PARA TRABALHAR COM A PARTE SINTATICA
# def createTable()

identificadores = []
def createParser():    
    #chamando o lexer
    lexerClass = myLexer()
    lexer = lexerClass.build()
    #pegando tokens
    tokens = lexerClass.getTokens()


    precedence = (
        ('left', 'OPSOMA', 'OPSUB'),
        ('left', 'OPMUL', 'OPDIV'),
    )
    #Programa e Bloco
    def p_programa(p):
        '''programa : PROGRAM ID FIM_LINHA bloco PONTO_FINAL 
                      
        '''


    def p_bloco(p):
        '''bloco : bloco parte_declaracao_de_variaveis 
                 | bloco parte_declaracao_de_subrotinas 
                 | comando_composto
                 | empty
        ''' 
        
    def p_parte_declaracao_de_variaveis(p):
        '''parte_declaracao_de_variaveis :  declaracao_de_variaveis FIM_LINHA parte_declaracao_de_variaveis
                                          | empty
        ''' 

    def p_declaracao_de_variaveis(p):
        '''declaracao_de_variaveis :  tipo_simples lista_de_identificadores
        ''' 
    

    def p_tipo_simples(p):
        '''tipo_simples : INT
                        | REAL
                        | BOOLEAN
        ''' 

    def p_lista_de_identificadores(p):
        '''lista_de_identificadores : ID mais_identificadores
        ''' 

    def p_mais_identificadores(p):
        '''mais_identificadores : SEPARADOR lista_de_identificadores
                                | empty
        ''' 

    def p_parte_declaracao_de_subrotinas(p):
        '''parte_declaracao_de_subrotinas : declaracao_de_procedimento FIM_LINHA
                                          | empty
        ''' 

    def p_declaracao_de_procedimento(p):
        '''declaracao_de_procedimento : PROCEDURE ID parametros_formais FIM_LINHA bloco
        ''' 

    def p_parametros_formais(p):
        '''parametros_formais : AP secao_parametros_formais FP
    
        ''' 
    def p_secao_parametros_formais(p):
        '''secao_parametros_formais : lista_de_identificadores DOIS_PONTOS tipo_simples FIM_LINHA secao_parametros_formais
                                    | lista_de_identificadores DOIS_PONTOS tipo_simples
                                    | VAR lista_de_identificadores DOIS_PONTOS tipo_simples
                                    | VAR lista_de_identificadores DOIS_PONTOS tipo_simples FIM_LINHA secao_parametros_formais
                                    | empty
    
        '''
    

    # COMANDOS 
    def p_comando_composto(p):
        '''comando_composto : BEGIN comandos END
        ''' 


    def p_comandos(p):
        '''comandos : comando FIM_LINHA comandos
                    | empty
        ''' 

    def p_comando(p):
        '''comando : atribuicao
                   | chamada_de_procedimento
                   | comando_composto
                   | comando_condicional_1
                   | comando_repetitivo_1
        ''' 

    def p_atribuicao(p):
        '''atribuicao : variavel OPIGUAL_ATRIB expressao
        ''' 

    def p_chamada_de_procedimento(p):
        '''chamada_de_procedimento : ID
                                   | ID AP lista_de_expressoes FP
        '''


    def p_comando_condicional_1(p):
        '''comando_condicional_1 : IF AP expressao FP THEN comando comando_condicional_falso_1
        '''

    def p_comando_condicional_falso_1(p):
        '''comando_condicional_falso_1 : ELSE comando
                                       | empty                             
        '''

    def p_comando_repetitivo_1(p):
        '''comando_repetitivo_1 : WHILE expressao DO comando
        '''


    def p_expressao(p): 
        '''expressao : expressao_simples     
                     | expressao_simples relacao expressao_simples
        ''' 


    def p_relacao(p):
        '''relacao : IGUAL     
                   | MAIOR_IGUAL
                   | MAIOR
                   | MENOR_IGUAL
                   | MENOR '''

    #seria o "expressao simples" definido no pdf
    def p_expressao_simples(p): 
        '''expressao_simples : expressao_simples OPSOMA termo
                             | expressao_simples OPSUB termo
                             | expressao_simples OR termo
                             | termo  
                
         '''


    def p_termo(p):
        '''termo : termo OPMUL fator
                 | termo OPDIV fator
                 | termo DIV fator
                 | termo AND fator
                 | fator


         '''
        


    def p_fator(p):
        '''fator : ID     
                 | numero
                 | AP expressao_simples FP
                 | NOT fator
        '''



    def p_variavel(p):
        '''variavel : ID     
                    | ID expressao
        ''' 
        # p[0] = p[1]

    def p_lista_de_expressoes(p):
        '''lista_de_expressoes : expressao mais_expressoes    
                              
        ''' 

    def p_mais_expressoes(p):
        '''mais_expressoes : SEPARADOR expressao
                        | empty  
                              
        '''

    def p_numero(p):
        '''numero : NUM_INT
                  | NUM_REAL 
                              
        '''
    def p_empty(p):
        'empty :'
        pass
         

    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input - " + str(p))


    parser = yacc.yacc(debug=True) 

    return parser

# while True:
#    try:
#        s = input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)