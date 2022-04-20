import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QMenu
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QTimer

class Example(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 200))    
        self.setWindowTitle("PyQt button example - pythonprogramminglanguage.com") 

        self.bt1 = QPushButton("Button 1",self)
        self.bt2 = QPushButton("Button 2",self)
        self.bt3 = QPushButton('Button 3',self)

        self.bt1.move(50,50)
        self.bt2.move(50,100)
        self.bt3.move(170,100)
        
        menu = QMenu(self)
        menu.addAction('Fruit')
        menu.addSeparator()
        menu.addAction('Cookies')
        menu.addSeparator()
        menu.addAction('Ice cream')
        self.bt2.setMenu(menu)

        self.bt1.clicked.connect(self.Button1)
        self.count = 10
        self.bt3.clicked.connect(self.Action)
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.show()

    def Button1(self):
        print('Clicked')
        
    def Action(self):
        if self.bt3.isEnabled():
            self.time.start()
            self.bt3.setEnabled(False)

    def Refresh(self):
        if self.count > 0:
            self.bt3.setText(str(self.count)+' seconds')
            self.count -= 1
        else:
            self.time.stop()
            self.bt3.setEnabled(True)
            self.bt3.setText('Button 3')
            self.count = 10

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Example()
    mainWin.show()
    sys.exit( app.exec_() )