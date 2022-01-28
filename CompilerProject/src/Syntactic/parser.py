# PARA CADA ESCOPO EXISTENTE, CASO TAL ESCOPO SEJA UMA PROCEDURE, O SEU REGISTRO
# ESTARÁ NO ESCOPO MAIS ACIMA.
# [ESCOPO1, ESCOPO2] - SE ESCOPO 2 FOR UMA PROCEDURE, SUA ASSINATURA ESTÁ REGISTRADA EM ESCOPO 1


# TODO - CORRIGIR BUG DE EMPILHAMENTO, PARA COMPARAÇÕES COM CONSTANTES À DIREITA (CONSTANTE SE TORNA PRIORIDADE) - EX a <= 0
# NO MOMENTO ESTÁ EMPLIHANDO 0 depois valor de a, e fazendo a operação <=, que resulta em 0 <= a.

import time
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from Lexic.LALGLex import myLexer


readFile = 'ReadWrite-Files/read.txt'
writeFile = 'ReadWrite-Files/write.txt'

# ESTRUTURAS DE TABELAS DE SIMBOLO

from Syntactic.SymbolTable import *
from Syntactic.Scope import *
from Syntactic.Errors import *


#GERACAO DE CODIGO
from CodeGeneration.CodeGeneration import *

# PARTES DA UI
from UI.MainWindow import *

# 32 shift/reduce é o normal



def createParser():  

    # ESTRUTURAS QUE CUIDAM DA ANALISE SEMANTICA 
    scopes = [] 
    begin_stack = []
    # objeto que controla os erros
    errors = Errors()  

    # ESTRUTURA DE AUXILIO NA GERACAO DE CODIGO
    codeGenerator = CodeGenerator()

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

    # ERRO AO INICIAR p_inicio_programa na linha de programa
    def p_programa(p):
        '''programa :  PROGRAM ID FIM_LINHA bloco comando_composto PONTO_FINAL fim_programa
        '''
        
        p[0] = p[4]
        

    # def p_inicio_programa(p):
    #     '''inicio_programa : 

    #     '''
    #     codeGenerator.iniciarPrograma(p[-1])

    def p_fim_programa(p):
        '''fim_programa : 

        '''
        codeGenerator.finalizarPrograma()
    def p_bloco(p):
        '''bloco : new_scope parte_declaracao_de_variaveis parte_declaracao_de_subrotinas
        ''' 


        p[0] = (p[1], p[2])

        
    #-- Declarando variaveis
    def p_parte_declaracao_de_variaveis(p):
        '''parte_declaracao_de_variaveis :  declaracao_de_variaveis FIM_LINHA parte_declaracao_de_variaveis
                                          | empty
        ''' 
        temp = [] #vai receber todas as tuplas ('tipo', var1, var2 ,..., varN)
        if(len(p) > 2):
            if(p[3] != None):
                temp.append(p[1])
                for each in p[3]:
                    temp.append(each)
            else:
                temp.append(p[1])

        p[0] = temp

        print('\n\nparte_declaracao_de_variaveis-debug: ', p[0])

    def p_declaracao_de_variaveis(p):
        '''declaracao_de_variaveis : tipo_simples lista_de_parametros
        ''' 
        
        print('declaracao_de_variaveis-debug: ', p[1], p[2])

        for variavel in p[2]:
            v = scopes[-1].variableTable.insert(variavel, p[1], p.lineno(1),False, None)
            if(v == errors.ERROR_VARIAVEL_JA_DECLARADA):
                error_message = "ERROR: A variavel '"+ str(variavel) +" ja foi declarada anteriormente - Linha: " + str(p.lineno(2))
                print(error_message)
                p_error(error_message)

            codeGenerator.declararVariavel(variavel, p[1])

        #print('declaracao_de_variaveis-debug-tabela: ', str(variaveis.table))

        p[0] = (p[1], p[2])

    def p_tipo_simples(p):
        '''tipo_simples : INT
                        | REAL
                        | BOOLEAN
        ''' 
        p[0] = p[1];

    #-- Declarando subrotinas - caso ocorram erros em declaracao de funcao, prestar atençao nos FIM_LINHA aqui
    def p_parte_declaracao_de_subrotinas(p):
        '''parte_declaracao_de_subrotinas : declaracao_de_procedimento
                                          | empty
        ''' 
        if(p[1] != None):
            p[0] = p[1]

        print('\nparte_declaracao_de_subrotinas-debug: ', p[0])

        print('\nparte_declaracao_de_subrotinas-debug-table: ', str(scopes[-1].procedureTable.table))
        scopes[-1].procedureTable.print_table()

    def p_declaracao_de_procedimento(p):
        '''declaracao_de_procedimento : PROCEDURE ID parametros_formais FIM_LINHA bloco comando_composto FIM_LINHA
        ''' 

        procedure = scopes[-1].procedureTable.insert(p[2], p[3], p[5][1])

        if(procedure == errors.ERROR_PROCEDURE_JA_DECLARADA):
            error_message = "ERROR: A procedure '"+ str(p[2]) +"' ja foi declarada - Linha: " + str(p.lineno(2))
            p_error(error_message)
        else:
            p[0] = (p[2], p[3], p[5][1], p[6]) #(id, parametros_formais, bloco, comando_composto)

        print('\ndeclaracao_de_procedimento - debug: ', p[5])

        
    # TALVEZ SEJA NECESSARIO COLOCAR O "VAR"
    def p_parametros_formais(p):
        '''parametros_formais : AP mais_parametros_formais FP
    
        ''' 
        p[0] = p[2]

        print('parametros_formais-debug: ', p[0])

    def p_mais_parametros_formais(p):
        '''mais_parametros_formais : FIM_LINHA lista_de_parametros DOIS_PONTOS tipo_simples mais_parametros_formais
                                    | lista_de_parametros DOIS_PONTOS tipo_simples mais_parametros_formais
                                    | empty
    
        '''
        temp = []
        if(len(p) == 6):
            temp.append((p[4], p[2])) #(tipo_simples, lista_de_parametros)
            if(p[5] != None):
                for each in p[5]:
                    temp.append(each)
            p[0] = temp
        if(len(p) == 5):
            temp.append((p[3], p[1]))
            if(p[4] != None):
                for each in p[4]:
                    temp.append(each)
            p[0] = temp

    # COMANDOS    
    def p_comando_composto(p):
        '''comando_composto : BEGIN new_begin comandos END
                            
        ''' 
        p[0] = p[2]

        begin_stack.pop()
        if(len(begin_stack) == 0):
            p_warnings(None)
            scopes.pop()

    #TRATAMENTO DE ESCOPOS 
    #==========================
    def p_new_scope(p):
        "new_scope :"
        temp_scope = Scope()
        scopes.append(temp_scope)


    def p_new_begin(p):
        "new_begin :"
        begin_stack.append("begin") 
    #==========================

    #TRATAMENTO DE AVISOS
    #============================================================================================================================================================
    def p_warnings(p):
        '''warnings : '''

        tabela_de_variaveis = scopes[-1].variableTable.table

        for variavel in tabela_de_variaveis:
            if(variavel['utilizada'] == False):
                errors.add_warning("WARNING: Variavel '"+ variavel['lexema'] +"' declarada e nao utilizada - Linha: " + str(variavel['linha']))
    #============================================================================================================================================================
               
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


    def p_atribuicao(p):
        '''atribuicao : variavel OPIGUAL_ATRIB expressao 
        ''' 
        
        temp = scopes[-1].variableTable.modify(p[1], p[3])

        if(temp == errors.ERROR_TIPO):
            error_message = "ERROR: O valor atribuido a variável '"+ str(p[1]) +"' não é compatível com o seu tipo - Linha: " + str(p.lineno(1))
            
            #chama a função de erro
            p_error(error_message)
            #raise SyntaxError
            
        elif(temp == errors.ERROR_VARIAVEL_NAO_DECLARADA):
            error_message = "ERROR: A variavel '" + str(p[1]) +"' não foi declarada - Linha: "+ str(p.lineno(1))

            p_error(error_message)
            #raise SyntaxError
        else:
            p[0] = temp

            codeGenerator.atribuicaoVariavel(p[1], p[3])
            
       

        print('atribuicao-debug', p[1], p[3])
        #print('atribuicao-debug-variaveis', str(variaveis.table))

    

    def p_comando_condicional_1(p):
        '''comando_condicional_1 : IF  AP expressao FP THEN verifica_IF comandos desvio_IF %prec IF 
                                 | IF  AP expressao FP THEN verifica_IF comandos desvio_IF ELSE verifica_ELSE comandos desvio_ELSE %prec ELSE
        '''
        
        if(len(p) == 9): #SE FOR SEM ELSE
            if(p[4]):
                p[0] = p[7] #recebe o comando
    
        

        else: #se for com else
            if(p[4]):
                p[0] = p[7]
            else:
                p[0] = p[9]
                
    # GERACAO DE CODIGO PARA IF STATEMENT
    # ====================================================
    def p_verifica_IF(p):
        ''' verifica_IF :
        '''
        codeGenerator.verificaIF()
    
    def p_desvio_IF(p):
        ''' desvio_IF :
        '''
        codeGenerator.desvioIF()

    def p_verifica_ELSE(p):
        ''' verifica_ELSE :
        '''
        codeGenerator.verificaElse()


    def p_desvio_ELSE(p):
        ''' desvio_ELSE :
        '''
        codeGenerator.desvioElse()
        
    # ====================================================


    def p_comando_repetitivo_1(p):
        '''comando_repetitivo_1 : WHILE AP set_expressao expressao verifica_WHILE FP DO comando_composto desvio_WHILE
        '''

        while(p[3]):
            p[0] = p[6]
            break 

    # GERACAO DE CODIGO PARA WHILE
    # ====================================================
    def p_set_expressao(p):
        '''set_expressao :  '''

        codeGenerator.setExpressao(codeGenerator.getContador())

    def p_verifica_WHILE(p):
        ''' verifica_WHILE :
        '''
        codeGenerator.verificaWhile()

    def p_desvio_WHILE(p):
        ''' desvio_WHILE :
        '''
        codeGenerator.desvioWhile()


    
    
    # ====================================================
    def p_chamada_de_procedimento(p):
        '''chamada_de_procedimento : variavel AP lista_de_parametros FP
                                   | READ AP lista_de_parametros FP
                                   | WRITE AP lista_de_parametros FP
        '''
        if(p[1] != None):
            lista_de_parametros = p[3]

            
            if(p[1] == 'read'):
                IS_OK = True
                #verificar se as variaveis existem
                for variavel in lista_de_parametros:
                    if(isinstance(variavel, str)): 
                        v = scopes[-1].variableTable.search(variavel)
                        if(v == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                            p_error("ERROR: A variavel '" + str(variavel) +"' não foi declarada - Linha: "+ str(p.lineno(1)))
                            #raise SyntaxError
                            IS_OK = False
                        
                        elif(scopes[-1].variableTable.get_tipo(variavel) != 'int'):
                            p_error("ERROR: A variavel '"+ str(variavel) + "' não e inteira (READ so aceita inteiros) - Linha: "+ str(p.lineno(1)))

                    else:
                        error_message = ("ERROR: Os parametros passados para a funcao READ, nao sao compativeis - Linha: "+ str(p.lineno(1)))
                        p_error(error_message)
                        print(error_message)
                        break

                if(IS_OK):
                    with open(readFile, 'r') as file:
                        valores = file.read()
                    valores = valores.split(" ")
                    
                    contador_valores = 0
                    if(len(valores) >= len(lista_de_parametros)):
                        codeGenerator.listaVariaveisRead(lista_de_parametros) # CODIGO DA LEITURA DAS VARIAVEIS
                        for parametro in lista_de_parametros:
                            p = scopes[-1].variableTable.modify(parametro, int(valores[contador_valores]))
                            print("chamada-de-procedimento-debug: variavel: " + str(parametro) + " valor: " + str(valores[contador_valores]))
                            contador_valores = contador_valores + 1
                    else:
                        error_message = "A lista de parametros para a procedure READ e o numero de valores no arquivo sao diferentes - Linha: " + str(p.lineno(1))

            elif(p[1] == 'write'): # verificar se a variavel que está sendo escrita, de fato existe
                codeGenerator.listaVariaveisWrite(lista_de_parametros, p.lexpos(3))
                with open(writeFile, 'w') as file:
                    for parametro in lista_de_parametros:
                        if(isinstance(parametro, str)): #se o parametro for uma variavel , busca ela
                            try:
                                value = scopes[-1].variableTable.get_value(parametro)

                                if(value == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                                    p_error("ERROR: A variavel '" + str(parametro) +"' não foi declarada - Linha: "+ str(p.lineno(1)))
                                
                                else:
                                    #file.write("Linha - " + str(p.lineno(1)) + ": " + str(value) + "\n")
                                    file.write(str(value) + " ")
                            except:
                                p_error("ERROR: A funcao WRITE aceita apenas variaveis como parametros.")
                        else:# se nao usa o valor
                            file.write(str(parametro) + " ")
            else:
                procedure = scopes[-1].procedureTable.search(p[1])

                if(procedure == errors.ERROR_PROCEDURE_NAO_DECLARADA):
                    error_message = "ERROR: A procedure '"+ str(p[1]) +"' nao foi declarada - Linha: " + str(p.lineno(1))
                    p_error(error_message)
                
                p[0] = p[1]


    def p_lista_de_parametros(p):
        '''lista_de_parametros : expressao mais_parametros
                               | empty
        ''' 
        lista_de_parametros1 = []
        if(len(p) > 2):
            if(p[2] != None):
                lista_de_parametros1.append(p[1])
                for parametro in p[2]:
                    lista_de_parametros1.append(parametro)

            else:
                lista_de_parametros1.append(p[1])

        p[0] = lista_de_parametros1
        

        print('lista_de_parametros-debug: ', p[0])


    def p_mais_parametros(p):
        '''mais_parametros : SEPARADOR lista_de_parametros
                            | empty
        ''' 

        if(len(p) > 2):
            p[0] = p[2]


    def p_expressao(p): 
        '''expressao : expressao_simples      
                     | expressao_simples relacao expressao_simples
        ''' 

        print("\n\nESCOPOS ATUAIS: ", str(scopes), '\n\n')

        if(len(p) > 2 and p[1] != None and p[3] != None):

            print('expressao-debug: ', p[1], p[2], p[3])

            if(isinstance(p[1], str)):  #CASO P[1] ESTEJA SE REFERINDO AO NOME DE UMA VARIAVEL, PEGAMOS SEU VALOR PARA REALIZAR O CALCULO
                codeGenerator.carregaValorDaVariavel(p[1], p.lexpos(1))
                v1 = scopes[-1].variableTable.get_value(p[1])
                
                if(v1 == errors.ERROR_VARIAVEL_SEM_VALOR): #caso a variavel nao tenha valor - Erro
                    p_error("ERROR: A variavel '" + p[1] + "' não tem valor definido - Linha: " + str(p.lineno(1)))
                    p[1] = -10000
                    #raise SyntaxError
                elif(v1 == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                    p_error("ERROR: A variavel '" + str(p[1]) +"' não foi declarada - Linha: "+ str(p.lineno(1)))
                    p[1] = -10000
                    #raise SyntaxError
                else:
                    p[1] = v1

            else:
                #codeGenerator.carregaValorConstante(p[1])
                pass

            if(isinstance(p[3], str)):  #O MESMO QUE PRO P[1]
                codeGenerator.carregaValorDaVariavel(p[3], p.lexpos(3))
                v2 = scopes[-1].variableTable.get_value(p[3])
                
                if(v2 == errors.ERROR_VARIAVEL_SEM_VALOR): #caso a variavel nao tenha valor - Erro
                    p_error("ERROR: A variavel '" + p[3] + "' não tem valor definido - Linha: " + str(p.lineno(3)))
                    p[3] = -10000
                    #raise SyntaxError
                elif(v2 == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                    p_error("ERROR: A variavel '" + str(p[3]) +"' não foi declarada - Linha: "+ str(p.lineno(3)))
                    p[3] = -10000 #recebe o "endereço de memoria"
                    #raise SyntaxError
                else: # caso a variavel tenha valor, atribuimos esse valor
                    p[3] = v2
            else:
                #codeGenerator.carregaValorConstante(p[3])  
                pass  

            codeGenerator.verificaRelacao(p[2])#

            resultado_relacao = None
            if(p[2] == '='):
                if(p[1] == p[3]):
                    resultado_relacao = True
                else:
                    resultado_relacao = False
            elif(p[2] == '>='):
                if(p[1] >= p[3]):
                    resultado_relacao = True
                else:
                    resultado_relacao = False
            elif(p[2] == '>'):
                if(p[1] > p[3]):
                    resultado_relacao = True
                else:
                    resultado_relacao = False 
            elif(p[2] == '<='):
                if(p[1] <= p[3]):
                    resultado_relacao = True
                else:
                    resultado_relacao = False 
            elif(p[2] == '<'):
                if(p[1] < p[3]):
                    resultado_relacao = True
                else:
                    resultado_relacao = False 
            elif(p[2] == '<>'):
                if(p[1] != p[3]):
                    resultado_relacao = True
                else:
                    resultado_relacao = False

            p[0] = resultado_relacao

        else:
            print('expressao-debug: ', p[1])  

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
        
            if(isinstance(p[1], str)):  #CASO P[1] ESTEJA SE REFERINDO AO NOME DE UMA VARIAVEL, PEGAMOS SEU VALOR PARA REALIZAR O CALCULO
                codeGenerator.carregaValorDaVariavel(p[1], p.lexpos(1))
                v1 = scopes[-1].variableTable.get_value(p[1])
                if(v1 == errors.ERROR_VARIAVEL_SEM_VALOR): #caso a variavel nao tenha valor - Erro
                    p_error("ERROR: A variavel '" + str(p[1]) + "' não tem valor definido - Linha: " + str(p.lineno(1)))
                    p[1] = -10000
                    #rai se SyntaxError
                elif(v1 == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                    p_error("ERROR: A variavel '" + str(p[1]) +"' não foi declarada - Linha: "+ str(p.lineno(1)))
                    p[1] = -10000
                    #raise SyntaxError
                else:
                    p[1] = v1
            else:
                # codeGenerator.carregaValorConstante(p[1])
                pass

            if(isinstance(p[3], str)):  #O MESMO QUE PRO P[1]
                codeGenerator.carregaValorDaVariavel(p[3], p.lexpos(3))
                v2 = scopes[-1].variableTable.get_value(p[3])
                if(v2 == errors.ERROR_VARIAVEL_SEM_VALOR): #caso a variavel nao tenha valor - Erro
                    p_error("ERROR: A variavel '" + p[3] + "' não tem valor definido - Linha: " + str(p.lineno(3)))
                    p[3] = -10000
                    #raise SyntaxError
                elif(v2 == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                    p_error("ERROR: A variavel '" + str(p[3]) +"' não foi declarada - Linha: "+ str(p.lineno(3)))
                    p[3] = -10000
                    #raise SyntaxError
                else: # caso a variavel tenha valor, atribuimos esse valor
                    p[3] = v2

            else:
                # codeGenerator.carregaValorConstante(p[3])
                pass

            

            if(p[2] == '+'):
                p[0] = p[1] + p[3]
            elif(p[2] == '-'):
                codeGenerator.inverterSinal()
                p[0] = p[1] - p[3]
            elif(p[2] == 'or'):
                p[0] = p[1] or p[3]

            codeGenerator.verificaOperador(p[2])
        else:   
            p[0] = p[1]
    


    def p_termo(p):
        '''termo : termo OPMUL fator
                 | termo OPDIV fator
                 | termo DIV fator
                 | termo AND fator
                 | fator
         '''

        divisao_inteira = False
        v1 = None
        v2 = None
        if(len(p) > 2 and p[1] != None and p[3] != None):

            print('termo-debug: ', p[1], p[2], p[3])

            if(isinstance(p[1], str)):  #CASO P[1] ESTEJA SE REFERINDO AO NOME DE UMA VARIAVEL, PEGAMOS SEU VALOR PARA REALIZAR O CALCULO
                codeGenerator.carregaValorDaVariavel(p[1], p.lexpos(1))
                v1 = scopes[-1].variableTable.get_value(p[1])
                
                if(v1 == errors.ERROR_VARIAVEL_SEM_VALOR): #caso a variavel nao tenha valor - Erro
                    p_error("ERROR: A variavel '" + p[1] + "' não tem valor definido - Linha: " + str(p.lineno(1)))
                    p[1] = -10000
                    #raise SyntaxError
                elif(v1 == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                    p_error("ERROR: A variavel '" + str(p[1]) +"' não foi declarada - Linha: "+ str(p.lineno(1)))
                    p[3] = -10000
                    #raise SyntaxError
                else:
                    p[1], v1 = v1, p[1]
            else:
                #codeGenerator.carregaValorConstante(p[1])
                pass

            if(isinstance(p[3], str)):  #O MESMO QUE PRO P[1]
                codeGenerator.carregaValorDaVariavel(p[3], p.lexpos(3))
                v2 = scopes[-1].variableTable.get_value(p[3])
                
                if(v2 == errors.ERROR_VARIAVEL_SEM_VALOR): #caso a variavel nao tenha valor - Erro
                    p_error("ERROR: A variavel '" + p[3] + "' não tem valor definido - Linha: " + str(p.lineno(3)))
                    p[3] = -10000
                    #raise SyntaxError
                elif(v2 == errors.ERROR_VARIAVEL_NAO_DECLARADA):
                    p_error("ERROR: A variavel '" + str(p[3]) +"' não foi declarada - Linha: "+ str(p.lineno(3)))
                    p[3] = -10000
                    #raise SyntaxError
                else: # caso a variavel tenha valor, atribuimos esse valor
                    p[3], v2 = v2, p[3]

            else:
                
                #codeGenerator.carregaValorConstante(p[3])
                pass

            codeGenerator.verificaOperador(p[2])

            if(isinstance(p[-2], str)): #verificando se é o caso de atribuicao ex : x := 45/y , nesse caso p[-2] = x
                if(scopes[-1].variableTable.get_tipo(p[-2]) == 'int'):
                    divisao_inteira = True

            if(p[2] == '*'):
                p[0] = p[1] * p[3]
            elif(p[2] == '/'):
                if(p[3] == 0):
                    p_error("ERROR: Zero Division - Linha: " + str(p.lineno(3)));
                    p[0] = p[1] #tratamento do erro
                else:
                    if(divisao_inteira):
                        p[0] = int(p[1] / p[3])
                    else:
                        p[0] = p[1]/p[3]
            elif(p[2] == 'and'):
                p[0] = p[1] and p[3]
            elif(p[2] == 'div'):
                if(p[3] == 0):
                    p_error("ERROR: Zero Division - Linha: " + str(p.lineno(3)));
                    p[0] = p[1] #tratamento do erro
                else:
                    p[0] = p[1] // p[3]

            

        else:  
            p[0] = p[1]

    def p_fator(p): #trocar "variavel" por "ID" evita muitos shift/reduce conflicts
        '''fator : numero  
                 | variavel 
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

        elif(p[1] == 'true' or p[1] == 'false'):
            if(p[1] == 'true'):
                p[0] = True
            else:
                p[0] = False

        else: # se for variavel ou numero
            if(isinstance(p[1], int) or isinstance(p[1], float)): #se for numero
                codeGenerator.carregaValorConstante(p[1], p.lexpos(1))
                p[0] = p[1]
            else: #se for variavel
                p[0] = p[1]

        


    def p_numero(p):
        '''numero : NUM_INT
                  | NUM_REAL 
                              
        '''
        p[0] = p[1]

    
    def p_variavel(p):
        '''variavel : ID     
        ''' 
        p[0] = p[1]

   
        
    def p_empty(p):
        'empty :'
        pass
         

    # Error rule for syntax errors
    
    def p_error(p):
        print("ENTREI AQ")
        if(isinstance(p, str)):
            print(str(p))
            #adiciona erro à lista de erros para serem exibidos na interface
            errors.add_error(p)
            
            # #tratamento para o parser continuar o trabalho, ignorando o erro, para que seja possivel exibir todos os erros ao mesmo tempo
            # while(True):
            #     tok = parser.token()
            #     print(tok.type)
            #     if(tok.type == 'FIM_LINHA'):
            #         tok = parser.token();
            #         break
            #     elif(not tok):
            #         break

            #tok = parser.token()

            #print(tok)

            parser.errok()

            #return tok

        else:
            
            if(p != None):
                print("ERRO DE SINTAXE - Token '" + str(p.value) + "' - LINHA " + str(p.lineno)) 
                errors.add_error("ERRO DE SINTAXE  - Token '" + str(p.value) + "' - LINHA " + str(p.lineno))
                
                while True:
                    tok = parser.token()         # Get the next token
                    if not tok or tok.type == 'PONTO_FINAL': break


                parser.errok()

            # else:
               
            #     print("ERRO DE SINTAXE  - EOF") 
            #     errors.add_error("ERRO DE SINTAXE  - EOF")

                

            

        

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