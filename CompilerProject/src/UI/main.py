from UI.MainWindow import *
import sys
#importando analisador lexico
from Lexic.LALGLex import *

#importando parser (analisador sintatico)
from Syntactic.parser import *
#importando classe de erros
from Syntactic.Errors import *
#importando gerador de codigo
from CodeGeneration.CodeGeneration import *
#importando interpretador de codigo
from Interpreter.Interpreter import *
#importando logger
from Syntactic.logger import*

#Importando componentes para a sintaxe
from PyQt5.QtCore import QFile, QRegExp, Qt, QSize, QObject
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor


# Chamando objeto Errors
errors = Errors()

# Chamando objeto gerador de codigo
codeGenerator = CodeGenerator()

# Chamando objeto Interpretador de codigo
codeInterpreter = Interpreter()

# Chamando objeto logger

logger = Logger()

# Line number Widget definition
class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, codeArea): 
        super().__init__(codeArea)
        self.codeArea = codeArea

        # Line Number Block WIDTH Constant
        LINE_NUMBER_WIDTH = 5 + self.fontMetrics().width('9') * 4

    def sizeHint(self):
        return self.QSize(self.codeArea.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeArea.lineNumberAreaPaintEvent(event)

# Code area QPlainTextEdit definition
class CodeArea(QtWidgets.QPlainTextEdit):
    def __init__(self, centralwidget):
        super().__init__(centralwidget)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        #self.updateLineNumberAreaWidth(0)
    
    # Updating the needed width to hold the numbers
    def lineNumberAreaWidth(self):
        digits = 1
        maximum = max(1, self.blockCount())
        while(maximum >= 10):
            maximum /= 10
            digits += 1

        space = 5 + self.fontMetrics().width('9') * digits

        return space

    def updateLineNumberAreaWidth(self, newBlockCount):
        
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
        
    # (self, QtCore.QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if(dy):
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())


        if(rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth(0)


    # Resizing the Number Area - Overriding method
    def resizeEvent(self, event):
        super().resizeEvent(event)

        #QRect
        cr = self.contentsRect()

        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        myPainter = QtGui.QPainter(self.lineNumberArea)

        myPainter.fillRect(event.rect(), QtCore.Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                myPainter.setPen(QtCore.Qt.black)
                myPainter.drawText(0, int(top), int(self.lineNumberArea.width()), int(height), QtCore.Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    def highlightCurrentLine(self):
        # List of QTextEdits
        extraSelections = []

        if(not self.isReadOnly()):
            selection = QtWidgets.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(185)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)



#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#

# Syntax Highlighter
class Highlighter(QSyntaxHighlighter):
    def __init__(self, textType, parent=None):
        super(Highlighter, self).__init__(parent)
        self.highlightingRules = [] #Setting the list of rules
        self.textType = textType #Setting the syntax highlighter type

    #Input syntax rules
    def inputRules(self):
        #Keywords format
        keyword = QTextCharFormat()
        keyword.setForeground(QColor('#00006e')) #Dark Blue
        keyword.setFontWeight(QFont.Bold)
        keywordPatterns = [r"\bint\b", r"\bfloat\b", r"\breal\b",r"\bboolean\b", r"\bvar\b",  r"\bprocedure\b", 
        r"\bbegin\b",  r"\bend\b", r"\bprogram\b", r"\bread\b", r"\bwrite\b"
        ]
        self.highlightingRules = [(QRegExp(pattern), keyword)
                for pattern in keywordPatterns]
        #Conditions and loops
        conditionAndLoops = QTextCharFormat()
        conditionAndLoops.setForeground(QColor('#920003')) #Red
        conditionAndLoops.setFontWeight(QFont.Bold)
        conditionAndLoopsPatterns = [r"\bwhile\b", r"\bfor\b", r"\bdo\b", r"\bif\b",  r"\belse\b", 
        r"\bthen\b"
        ]
        self.highlightingRules += [(QRegExp(pattern), conditionAndLoops)
                for pattern in conditionAndLoopsPatterns]
        
        #Numbers Format
        number = QTextCharFormat()
        number.setForeground(QColor('#00b0f4')) #Cyan
        self.highlightingRules.append((QRegExp(r"\b\d+\b|\btrue\b|\bfalse\b"),
                number))

        # Operators format
        operator = QTextCharFormat()
        operator.setForeground(QColor('#646464')) #Gray
        self.highlightingRules.append((QRegExp(r"[\+\-\*/<>=:()]|\bdiv\b"),
                operator))

        #Comment Format
        singleLineComment = QTextCharFormat()
        singleLineComment.setForeground(Qt.lightGray)
        self.highlightingRules.append((QRegExp("//[^\n]*"),
                singleLineComment))

        self.multiLineComment = QTextCharFormat()
        self.multiLineComment.setForeground(Qt.lightGray)

        self.commentStartExpression = QRegExp(r"\{")
        self.commentEndExpression = QRegExp(r"\}")

    #Output syntax rules
    def outputRules(self):
        #Any
        anyChar = QTextCharFormat()
        anyChar.setForeground(QColor('#282828')) #Black
        anyChar.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegExp(r"."),
                anyChar))

        #Variable Type
        variable = QTextCharFormat()
        variable.setForeground(QColor('#00006e')) #Dark Blue
        variable.setFontWeight(QFont.Bold)
        variablePatterns = [r"\bint\b", r"\bfloat\b", r"\bdouble\b", r"\bboolean\b, \bprocedure\b", r"\bprogram\b", 
        r"\bbegin\b", r"\bend\b", r"\bvar\b"
        ]

        for pattern in variablePatterns:
            self.highlightingRules.append((QRegExp(pattern),
                variable))

        #condition Type
        condition = QTextCharFormat()
        condition.setForeground(QColor('#920003')) #Red
        condition.setFontWeight(QFont.Bold)
        conditionPatterns = [r"\bif\b", r"\belse\b", r"\bthen\b", r"\bwhile\b", r"\bfor\b",
        ]
        for pattern in conditionPatterns:
            self.highlightingRules.append((QRegExp(pattern),
                condition))

        #WARNING
        warning = QTextCharFormat()
        warning.setForeground(QColor('#F29F18')) #Yellow
        self.highlightingRules.append((QRegExp(r"(?=WARNING:).*"),
                warning))

        #numbers
        numbers = QTextCharFormat()
        numbers.setForeground(QColor('#00b0f4')) #Gray
        self.highlightingRules.append((QRegExp(r"\b\d+\b|\bdiv\b"),
                numbers))


        #Symbols
        Symbols = QTextCharFormat()
        Symbols.setForeground(QColor('#F0750F')) #Yellow
        self.highlightingRules.append((QRegExp(r"[\W]|\bdiv\b"),
                Symbols))

        #Lexic Pointer
        LexicPointer = QTextCharFormat()
        LexicPointer.setForeground(QColor('#1C1C1C')) #Purble
        self.highlightingRules.append((QRegExp(r'(?==>).*'),
                LexicPointer))

        #Line Number
        line = QTextCharFormat()
        line.setForeground(QColor('#646464')) #Green
        self.highlightingRules.append((QRegExp(r"^LINHA.*"),
                line))


    #QSyntaxHighlighter Function to paint the Regex rules
    def highlightBlock(self, text):
        #Painting the input rules
        if(self.textType == 'input'):
            for pattern, format in self.highlightingRules:
                expression = QRegExp(pattern)
                index = expression.indexIn(text)
                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)

            #Comment rule
            startIndex = 0
            if self.previousBlockState() != 1:
                startIndex = self.commentStartExpression.indexIn(text)

            while startIndex >= 0:
                endIndex = self.commentEndExpression.indexIn(text, startIndex)

                if endIndex == -1:
                    self.setCurrentBlockState(1)
                    commentLength = len(text) - startIndex
                else:
                    commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

                self.setFormat(startIndex, commentLength,
                        self.multiLineComment)
                startIndex = self.commentStartExpression.indexIn(text,
                        startIndex + commentLength);

        #Painting the output rules
        elif(self.textType == 'output'):
            for pattern, format in self.highlightingRules:
                expression = QRegExp(pattern)
                index = expression.indexIn(text)
                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)


# Definir highlighter para o output
#class OutputHighlighter(Highlighter):

#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------#

# CLASS TO EXECUTE THE UI

class ExecWindow(Ui_MainWindow):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.lexer = None
        self.parser = None
        self.setupUi(self.window)
        self.connectActions()
        

    # ADD WINDOW CHARACTERISTICS HERE
    def setupUi(self, window):
        super().setupUi(self.window)
        
        # Setting window properties
        self.window.setWindowIcon(QtGui.QIcon('icons/windowIcon.png'))
        #Window Flags (Disable resize)
        self.window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.window.setStyleSheet("background-color: white;")
        self.window.setFixedSize(self.window.frameGeometry().width(), self.window.frameGeometry().height()) #TAMANHO FIXO

        # Creating Code Area with Line Number
        self.textInput = CodeArea(self.centralwidget)
        self.textInput.setGeometry(QtCore.QRect(20 , 50, 841, 451))
        self.textInput.setObjectName("textInput")

        # Setting tab distance
        self.textInput.setTabStopDistance(QtGui.QFontMetricsF(self.textInput.font()).horizontalAdvance(' ') * 4)

        # Setting syntax colors for textInput
        self.highlighter = Highlighter('input', self.textInput.document())
        self.highlighter.inputRules()

        # Setting syntax colors for textOutput
        self.highlighter2 = Highlighter('output', self.textOutput.document())
        self.highlighter2.outputRules()

        # Setting buttons properties
        pixmap = QtGui.QPixmap("icons/analyze.png")
        analyze_icon = QtGui.QIcon(pixmap)
        self.analyzeButton.setIcon(analyze_icon)
        self.analyzeButton.setIconSize(QSize(23, 23))
        self.analyzeButton.setStyleSheet(
        """
        QPushButton
        {
        background-color: #D0D0D0;
        border-radius: 15px;
        }
        QPushButton::hover
        {
        background-color: #9A9A9A;
        }
        """
        )

        pixmap = QtGui.QPixmap("icons/build.png")
        compile_icon = QtGui.QIcon(pixmap)
        self.compileButton.setIcon(compile_icon)
        self.compileButton.setIconSize(QSize(23, 23))
        self.compileButton.setStyleSheet(
        """
        QPushButton
        {
        background-color: #D0D0D0;
        border-radius: 15px;
        }
        QPushButton::hover
        {
        background-color: #9A9A9A;
        }
        """
        )

        # Setting fonts and styles of the text
        self.textInput.setFont(QFont("Courier New", 12))
        self.textOutput.setFont(QFont("Courier New", 12))

        # Setting Menu properties
        # Shortcuts
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionSave.setShortcut("Ctrl+S")
        self.menuBar.setStyleSheet(
        """
        QMenuBar
        {
            background-color: lightGray;
            color: #000;
        }
        QMenuBar::item
        {
            background-color: lightGray;
            color: #000;
        }
        QMenuBar::item::selected
        {
            background-color: Gray;
            color: #000;
        }
        QMenu
        {
            background-color: lightGray;
            color: #000;
        }
        QMenu::item::selected
        {
            background-color: Gray;
            color: #000;
        }
         """
        )
            
    
    def connectActions(self):
        # pressing the analyze button
        self.analyzeButton.clicked.connect(lambda: self.lexicAnalyze())
        # pressing the compile button - open parser (Syntactic Analyze)
        self.compileButton.clicked.connect(lambda: self.parse())

        # Handling Open and Save Files cases
        self.actionOpen.triggered.connect(lambda: self.openFile())
        self.actionSave.triggered.connect(lambda: self.saveFile())


    # Lexical Analysis Function
    def lexicAnalyze(self):
        self.lexer = myLexer(self.textOutput)
        self.lexer.build()
        # Passando o texto de input
        text = self.textInput.toPlainText()
        
        self.lexer.use(text)

    # Parsing Function (Syntactic Analysis)
    def parse(self):
        self.parser = createParser()

        #pegando o input e jogando no parser que foi criado utilizando o analisador lexico
        text = self.textInput.toPlainText()

        #calculando resultado e exibindo na tela de output - se não for "None"
        
        result = self.parser.parse(text, tracking=True, debug=logger.getLog())


        
        # condição para exibição na caixa de texto de output
        if(result != None):  # caso retorne algo diferente de None, ou seja, existe um resultado, não tivemos erros
            error_list = ""
            

            #print(errors.get_errorList())
            #INCUINDO ERROS NO OUTPUT
            if(errors.has_errors()):  #SE TIVER ERROS, EXIBE APENAS OS ERROS
                for error in errors.get_errorList():
                    error_list = error_list + error + "\n"
                errors.clear_errors() 

                self.textOutput.setText("")
                self.textOutput.setText(error_list)
            else:
                result = str(result) + "\n"
                # INCLUINDO WARNINGS NO OUTPUT
                for warning in errors.get_warningList():
                    result = result + warning + "\n"
                errors.clear_warnings()


                self.textOutput.setText("")
                self.textOutput.setText(str(result))

                #GERA CODIGO INTERMEDIARIO
                codeGenerator.salvarEmArquivo("codigoIntermediario.txt")
                #INTERPRETA CODIGO INTERMEDIARIO
                codeInterpreter.readFile("codigoIntermediario.txt")
                output = codeInterpreter.execute(self.window)

                self.textOutput.setText("")
                self.textOutput.setText(str(output))

        else: # caso existirem erros
             # INCLUINDO ERROS NO OUTPUT
            error_list = ""
            if(errors.has_errors()): #SE TIVER ERROS, EXIBE APENAS OS ERROS
                for error in errors.get_errorList():
                    error_list = error_list + error + "\n"
                errors.clear_errors() 

                self.textOutput.setText("")
                self.textOutput.setText(error_list)
            
            else:
                # INCLUINDO WARNINGS NO OUTPUT
                for warning in errors.get_warningList():
                    error_list = error_list + warning + "\n"
                errors.clear_warnings()
                
                self.textOutput.setText("")
                self.textOutput.setText(error_list)

                #GERA CODIGO INTERMEDIARIO
                codeGenerator.salvarEmArquivo("codigoIntermediario.txt")
                #INTERPRETA CODIGO INTERMEDIARIO
                codeInterpreter.readFile("codigoIntermediario.txt")
                output = codeInterpreter.execute(self.window, self.textOutput)

                self.textOutput.setText("")
                self.textOutput.setText(str(output))
        return


    # Opening a File
    def openFile(self):
        text = ""
        filename = QtWidgets.QFileDialog.getOpenFileName()[0]
        try:
            with open(filename, "r") as f:
                for line in f:
                    text = text + line

            self.textInput.setPlainText(text)
        except:
            pass

    # Saving a File
    def saveFile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName()[0]
        try:
            with open(filename, "w+") as f:
                f.write(self.textInput.toPlainText())
        except:
            pass
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()
    ExecWindow(window)

    window.show()
    app.exec()