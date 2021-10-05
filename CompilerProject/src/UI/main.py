from UI.MainWindow import *
import sys
#importando analisador lexico
from Lexic.lexer import * 





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
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)

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
        with open(filename, "r") as f:
            for line in f:
                text = text + line

        self.textInput.setPlainText(text)

    # Saving a File
    def saveFile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName()[0]
        with open(filename, "w+") as f:
            f.write(self.textInput.toPlainText())
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()
    ExecWindow(window)

    window.show()
    app.exec()