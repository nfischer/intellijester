#!/usr/bin/python

from PyQt4 import QtGui, QtCore
import sys

# Import the interface class
import Screen1
import Screen2

class Screen1Main(QtGui.QMainWindow, Screen1.Ui_MainWindow):
    """ The second parent must be 'Ui_<obj. name of main widget class>'.
    If confusing, simply open up ImageViewer.py and get the class
    name used. I'd named mine as mainWindow, hence Ui_mainWindow. """

    def __init__(self, parent=None):
        super(Screen1Main, self).__init__(parent)
        # This is because Python does not automatically
        # call the parent's constructor.
        self.setupUi(self)
        # Pass this "self" for building widgets and
        # keeping a reference.
        self.pushButton.clicked.connect(self.handleButton)
        self.window2 = None


    def main(self):
        self.show()


    def handleButton(self):

        self.window2 = Screen2Main(self)
        self.window2.show()


class Screen2Main(QtGui.QMainWindow, Screen2.Ui_MainWindow):
    def __init__(self,parent=None):
        super(Screen2Main,self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.handleButton)
    def handleButton(self):

        self.window1 = Screen1Main(self)
        self.window1.show()


if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    imageViewer = Screen1Main()
    imageViewer.main()
    app.exec_()
      # This shows the interface we just created. No logic has been added, yet.
