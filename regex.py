import sys
from PyQt5 import QtWidgets , QtGui 
import re
import time

class LearnRegex(QtWidgets.QWidget):
    def __init__(self):
        super(LearnRegex,self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(720,640)
        self.setWindowTitle("ReGex Learner")
        self.setFont(QtGui.QFont('Arial',12))

        self.txtPattern = QtWidgets.QLineEdit()
        self.txtReplace = QtWidgets.QLineEdit()
        self.txtText = QtWidgets.QPlainTextEdit()
        self.txtResult = QtWidgets.QPlainTextEdit()

        self.regex = None
        self.regexText = None
        self.flag = False

        lblPattern = QtWidgets.QLabel('Pattern\t')
        lblReplace = QtWidgets.QLabel('Replace Pattern\t')
        lblText = QtWidgets.QLabel('Text\t')
        lblResult = QtWidgets.QLabel('Result\t')

        btnMatch = QtWidgets.QPushButton('Match')
        btnNextMatch = QtWidgets.QPushButton('Next Match')
        btnReplace = QtWidgets.QPushButton('Replace')
        btnSplit = QtWidgets.QPushButton('Split')
        btnExit = QtWidgets.QPushButton('Exit')
        
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lblPattern,1,0)
        grid.addWidget(self.txtPattern, 1, 1, 1, 5)

        grid.addWidget(lblReplace,2,0)
        grid.addWidget(self.txtReplace, 2, 1, 1, 5)

        grid.addWidget(lblText,3,0)
        grid.addWidget(self.txtText, 3, 1, 1, 5)

        grid.addWidget(lblResult,5,0)
        grid.addWidget(self.txtResult, 5, 1, 1, 5)

        grid.addWidget(btnMatch, 4, 1)
        grid.addWidget(btnNextMatch, 4, 2)
        grid.addWidget(btnReplace, 4, 3)
        grid.addWidget(btnSplit, 4, 4)
        grid.addWidget(btnExit, 4, 5)

        btnMatch.clicked.connect(self.match_click)
        btnNextMatch.clicked.connect(self.nextmatch_click)
        btnReplace.clicked.connect(self.replace_click)
        btnSplit.clicked.connect(self.split_click)
        btnExit.clicked.connect(self.exit_click)

        btnMatch.setStyleSheet(
            "QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        btnNextMatch.setStyleSheet(
            "QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        btnReplace.setStyleSheet(
            "QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        btnSplit.setStyleSheet(
            "QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")
        btnExit.setStyleSheet(
            "QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")

        self.setWindowIcon(QtGui.QIcon('regex1.jpg'))

        self.setLayout(grid) 
        self.show()
    
    def exit_click(self):
        exit(0)

    def match_click(self):
        self.flag=False
        self.txtResult.setPlainText('Value\tLocation\tLength\tTime Taken')
        try:
            self.regex = re.compile(self.txtPattern.text())
        except Exception as e:
            return
        
        self.regex_text = self.txtText.toPlainText()
        self.regex_group = dict((v,k) for k,v in self.regex.groupindex.items())
        self.match_iter = self.regex.finditer(self.regex_text)
        self.highlight_text()
        
    def nextmatch_click(self):
        self.highlight_text()

    def replace_click(self):
        self.txtResult.setPlainText(f"Replaced Text After Changing {self.txtPattern.text()} with {self.txtReplace.text()} :-")
        self.txtResult.appendPlainText(
            re.sub(self.txtPattern.text(),self.txtReplace.text(),self.txtText.toPlainText()))
        
    def split_click(self):
        self.txtResult.setPlainText(f"Text After Spliting :-")
        for s in re.split(self.txtPattern.text(), self.txtText.toPlainText()):
            self.txtResult.appendPlainText(s)
    
    def highlight_text(self):
        begin_time = None
        try:
            # self.txtText.setPlainText(self.regexText)
            begin_time = time.time()
            match = self.match_iter.__next__()
            end_time = time.time()
            self.txtResult.appendPlainText(f'{match.group(0)}\t{match.start()}\t{match.end()-match.start()}\t{end_time-begin_time}')
            if match:
                for i in range(0,len(match.groups())):
                    groupNo = i+1
                    groupName = None
                    if groupNo in self.regex_group:
                        groupName = self.regex_group[groupNo]

                    self.txtResult.appendPlainText(f'Group : {groupNo}\tName : {groupName}\tValue : {match.group(groupNo)}')

                self.highlighter(match.start(),match.end())
            
        except:
            end_time =time.time()
            if not self.flag:
                self.txtResult.appendPlainText('End, Elapsed Time (s): {0:0.6f}'.format(end_time - begin_time)) 
                self.flag=True

    def highlighter(self,start,end):
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("lightgreen")))
        cursor = self.txtText.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,end-start)
        cursor.mergeCharFormat(format) 

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = LearnRegex()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()