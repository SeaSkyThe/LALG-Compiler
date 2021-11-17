# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from Lexic.LALGLex import myLexer


def createParser():    
    #chamando o lexer
    lexerClass = myLexer()
    lexer = lexerClass.build()
    #pegando tokens
    tokens = lexerClass.getTokens()


    #operacoes aritimeticas  
    def p_expression(p):
        '''expression : expression OPSOMA term
                      | expression OPSUB term
                      | expression OPMUL factor
                      | expression OPDIV factor'''
        
        if(p[2] == '+'):
            p[0] = p[1] + p[3]

        elif(p[2] == '-'):
            p[0] = p[1] - p[3]

        elif(p[2] == '*'):
            p[0] = p[1] * p[3]

        elif(p[2] == '/'):
            p[0] = p[1] / p[3]
     

    def p_expression_term(p):
        'expression : term'
        p[0] = p[1]

    def p_term_factor(p):
        'term : factor'
        p[0] = p[1]

    def p_factor_num(p):
        'factor : INT'
        p[0] = p[1]

    def p_factor_expr(p):
        'factor : AP expression FP'
        p[0] = p[2]



    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")


    parser = yacc.yacc() 

    return parser

# while True:
#    try:
#        s = input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)