from UI.MainWindow import *
import sys
#importando analisador lexico
from Lexic.lexer import * 
#Importando componentes para a sintaxe
from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor




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
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        #Keywords format
        keyword = QTextCharFormat()
        keyword.setForeground(QColor('#229bdd'))
        keyword.setFontWeight(QFont.Bold)
        keywordPatterns = [r"\bint\b", r"\bfloat\b", r"\bboolean\b", r"\bvar\b",  r"\bprocedure\b", 
        r"\bbegin\b",  r"\bend\b", r"\bprogram\b"
        ]
        self.highlightingRules = [(QRegExp(pattern), keyword)
                for pattern in keywordPatterns]

        #Conditions and loops
        conditionAndLoops = QTextCharFormat()
        conditionAndLoops.setForeground(QColor('#d11f1f'))
        conditionAndLoops.setFontWeight(QFont.Bold)
        conditionAndLoopsPatterns = [r"\bwhile\b", r"\bfor\b", r"\bdo\b", r"\bif\b",  r"\belse\b", 
        r"\bthen\b"
        ]
        self.highlightingRules += [(QRegExp(pattern), conditionAndLoops)
                for pattern in conditionAndLoopsPatterns]
        
        #Numbers Format
        number = QTextCharFormat()
        number.setForeground(QColor('#8f3dd6'))
        self.highlightingRules.append((QRegExp(r".\W\d+|\btrue\b|\bfalse\b"),
                number))

        # Operators format
        operator = QTextCharFormat()
        operator.setForeground(QColor('#d11f1f'))
        self.highlightingRules.append((QRegExp(r"[\+\-\*/<>=:]"),
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


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

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

        self.setupUi(self.window)
        self.connectActions()
    
    # ADD WINDOW CHARACTERISTICS HERE
    def setupUi(self, window):
        super().setupUi(self.window)
        
        # Setting window icon
        self.window.setWindowIcon(QtGui.QIcon('UI/icons8-svelte-48.png'))

        # Creating Code Area with Line Number
        self.textInput = CodeArea(self.centralwidget)
        self.textInput.setGeometry(QtCore.QRect(20 , 50, 841, 451))
        self.textInput.setObjectName("textInput")
        # Setting tab distance
        self.textInput.setTabStopDistance(QtGui.QFontMetricsF(self.textInput.font()).horizontalAdvance(' ') * 4)

        # Setting syntax colors
        self.highlighter = Highlighter(self.textInput.document())

        # Setting buttons icons
        pixmap = QtGui.QPixmap("UI/botao-play.png")
        compile_icon = QtGui.QIcon(pixmap)
        self.analyzeButton.setIcon(compile_icon)
        self.analyzeButton.setIconSize(self.analyzeButton.size())


        # Setting fonts and styles of the text


    
    
    def connectActions(self):
        # pressing the analyze button
        self.analyzeButton.clicked.connect(lambda: self.analyze())
        # Handling Open and Save Files cases
        self.actionOpen.triggered.connect(lambda: self.openFile())
        self.actionSave.triggered.connect(lambda: self.saveFile())


    # Lexical Analysis Function
    def analyze(self):
        lexer = MyLexer(self.textOutput)
        lexer.build()
        # Passando o texto de input
        text = self.textInput.toPlainText()
        lexer.use(text)

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