from UI.MainWindow import *
import sys
#importando analisador lexico
from Lexic.lexer import * 

class execWindow(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()
        self.setupUi(window)
        self.connectActions()
        
    def connectActions(self):
        self.analyzeButton.clicked.connect(lambda: self.analyze())

    def analyze(self):
        # #criando uma instancia da classe de criação do analisador lexico
        # lexerClass = createLexerClass()
        # #pegando o analisador lexico
        # lexer = lexerClass.getLexer()
        # #passando o input para o lexer
        # text = self.textInput.toPlainText()
        # lexer.input(text)
        
        # #criando o output a ser exibido
        # output = ''
        # tokensExtenso = lexerClass.getTokensExtenso()
        # for token in lexer:
        #     output = output + str(token.value) + " => " + str(tokensExtenso[token.type]) +"\n"
        # self.textOutput.setText(output)
        # return text
        #

        #  TODO
        # IMPORTANTE: CRIANDO UM ANALISADOR LEXICO A CADA CLIQUE NO BOTAO, FUTURAMENTE PODE SER PRECISO PRESTAR ATENCAO NISSO.
        # Criando o analisador lexico
        lexer = MyLexer(self.textOutput)
        lexer.build()
        # Passando o texto de input
        text = self.textInput.toPlainText()
        lexer.use(text)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()
    execWindow(window)

    window.show()
    app.exec()