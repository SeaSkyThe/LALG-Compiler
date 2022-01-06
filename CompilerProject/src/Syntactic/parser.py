#TODO, DECLARACAO DE VARIAVEIS

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from Lexic.LALGLex import myLexer


readFile = 'ReadWrite-Files/read.txt'
writeFile = 'ReadWrite-Files/write.txt'

# FUNÇÕES PARA TRABALHAR COM A PARTE SINTATICA
# def createTable()


# 32 shift/reduce é o normal

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
        ('left', 'IF'), 
        ('left', 'ELSE'),
        ('left', 'BEGIN'),
        ('left', 'INT', 'REAL', 'BOOLEAN'),

 
    )
    #Programa e Bloco - POR ENQUANTO ESTÁ OBRIGATORIO O PROGRAMA TER "Begin End."
    def p_programa(p):
        '''programa : PROGRAM ID FIM_LINHA bloco comando_composto PONTO_FINAL 
                      
        '''

        p[0] = p[4]

    def p_bloco(p):
        '''bloco : parte_declaracao_de_variaveis parte_declaracao_de_subrotinas
        ''' 

        p[0] = p[1]

    #-- Declarando variaveis
    def p_parte_declaracao_de_variaveis(p):
        '''parte_declaracao_de_variaveis :  declaracao_de_variaveis FIM_LINHA parte_declaracao_de_variaveis
                                          | empty
        ''' 

    def p_declaracao_de_variaveis(p):
        '''declaracao_de_variaveis : tipo_simples lista_de_parametros
        ''' 
    
    def p_tipo_simples(p):
        '''tipo_simples : INT
                        | REAL
                        | BOOLEAN
        ''' 


    #-- Declarando subrotinas - caso ocorram erros em declaracao de funcao, prestar atençao nos FIM_LINHA aqui
    def p_parte_declaracao_de_subrotinas(p):
        '''parte_declaracao_de_subrotinas : declaracao_de_procedimento
                                          | empty
        ''' 

    def p_declaracao_de_procedimento(p):
        '''declaracao_de_procedimento : PROCEDURE ID parametros_formais FIM_LINHA bloco comando_composto FIM_LINHA
        ''' 


    # TALVEZ SEJA NECESSARIO COLOCAR O "VAR"
    def p_parametros_formais(p):
        '''parametros_formais : AP mais_parametros_formais FP
    
        ''' 


    def p_mais_parametros_formais(p):
        '''mais_parametros_formais : FIM_LINHA lista_de_parametros DOIS_PONTOS tipo_simples mais_parametros_formais
                                    | lista_de_parametros DOIS_PONTOS tipo_simples mais_parametros_formais
                                    | empty
    
        '''


    # COMANDOS    
    def p_comando_composto(p):
        '''comando_composto : BEGIN comandos END 
                            
        ''' 
        p[0] = p[2]

    def p_comandos(p):
        '''comandos : atribuicao FIM_LINHA comandos
                    | chamada_de_procedimento FIM_LINHA comandos
                    | comando_composto comandos
                    | comando_condicional_1 comandos
                    | comando_repetitivo_1 comandos
                    | empty
        ''' 

        if(len(p) == 4):
            p[0] = (p[1], p[3])

        if(len(p) == 3):
            p[0] = (p[1], p[2])


    #TODO - FAZER O TRATAMENTO DE VARIAVEIS
    def p_atribuicao(p):
        '''atribuicao : variavel OPIGUAL_ATRIB expressao
        ''' 
        p[0] = p[3]


    def p_comando_condicional_1(p):
        '''comando_condicional_1 : IF AP expressao FP THEN comandos  %prec IF 
                                 | IF AP expressao FP THEN comandos ELSE comandos %prec ELSE
        '''

        if(len(p) == 7): #SE FOR SEM ELSE
            if(p[3]):
                p[0] = p[6] #recebe o comando

        if(len(p) > 7): #se for com else
            if(p[3]):
                p[0] = p[6]
            else:
                p[0] = p[8]


    #TODO - FAZER O LOOP CORRETO DE ACORDO COM A CONDIÇÃO
    def p_comando_repetitivo_1(p):
        '''comando_repetitivo_1 : WHILE AP expressao FP DO comandos
        '''

        while(p[3]):
            p[0] = p[6]
            break 

    #TODO - FAZER TODA A VERIFICAÇÃO DE PROCEDIMENTOS E VERIFICAR QUAL A EXECUÇÃO CORRETA - problema com 1 parametro
    def p_chamada_de_procedimento(p):
        '''chamada_de_procedimento : variavel AP lista_de_parametros FP
        '''
        if(p[1] != None):
            p[0] = p[1]

    def p_lista_de_parametros(p):
        '''lista_de_parametros : expressao mais_parametros
                               | empty
        ''' 

        if(len(p) > 2):
            p[0] = (p[1], p[2])

    def p_mais_parametros(p):
        '''mais_parametros : SEPARADOR lista_de_parametros
                            | empty
        ''' 
        if(len(p) > 2):
            p[0] = p[1]


    def p_expressao(p): 
        '''expressao : expressao_simples     
                     | expressao_simples relacao expressao_simples
        ''' 
        if(len(p) > 2 and p[1] != None and p[3] != None):
            if(p[2] == '<>'):
                if(p[1] == p[3]):
                    p[0] = True
                else:
                    p[0] = False
            elif(p[2] == '>='):
                if(p[1] >= p[3]):
                    p[0] = True
                else:
                    p[0] = False
            elif(p[2] == '>'):
                if(p[1] > p[3]):
                    p[0] = True
                else:
                    p[0] = False 
            elif(p[2] == '<='):
                if(p[1] <= p[3]):
                    p[0] = True
                else:
                    p[0] = False 
            elif(p[2] == '<'):
                if(p[1] < p[3]):
                    p[0] = True
                else:
                    p[0] = False 
        else:
            p[0] = p[1]
        
    def p_relacao(p):
        '''relacao : IGUAL     
                   | MAIOR_IGUAL
                   | MAIOR
                   | MENOR_IGUAL
                   | MENOR '''
        p[0] = p[1]

    #seria o "expressao simples" definido no pdf
    def p_expressao_simples(p): 
        '''expressao_simples : expressao_simples OPSOMA termo
                             | expressao_simples OPSUB termo
                             | expressao_simples OR termo
                             | termo  
                
         '''
        if(len(p) > 2 and p[1] != None and p[3] != None):
            if(p[2] == '+'):
                p[0] = p[1] + p[3]
            elif(p[2] == '-'):
                p[0] = p[1] - p[3]
            elif(p[2] == 'or'):
                p[0] = p[1] or p[3]
        else: 
            p[0] = p[1]


    def p_termo(p):
        '''termo : termo OPMUL fator
                 | termo OPDIV fator
                 | termo DIV fator
                 | termo AND fator
                 | fator
         '''
        if(len(p) > 2 and p[1] != None and p[3] != None):
            if(p[2] == '*'):
                p[0] = p[1] * p[3]
            elif(p[2] == '/'):
                p[0] = p[1] / p[3]
            elif(p[2] == 'and'):
                p[0] = p[1] and p[3]
        else:
            p[0] = p[1]

    def p_fator(p): #trocar "variavel" por "ID" evita muitos shift/reduce conflicts
        '''fator : variavel   
                 | numero
                 | TRUE
                 | FALSE
                 | AP expressao_simples FP
                 | NOT fator
        '''
        if(len(p) > 2):
            if(len(p) == 4): #expressao com parenteses
                p[0] = p[2]
            if(len(p) == 3): #expressao com NOT
                p[0] = not p[2]

        else: # se for variavel ou numero
            if(isinstance(p[1], int)):
                p[0] = p[1]


    def p_numero(p):
        '''numero : NUM_INT
                  | NUM_REAL 
                              
        '''
        p[0] = p[1]

    #TODO - SISTEMA DE VARIAVEIS
    def p_variavel(p):
        '''variavel : ID     
        ''' 
        # p[0] = p[1]

   
        
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