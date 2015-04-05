
#!/usr/bin/python
 
from PyQt4 import QtGui, QtCore
import sys

# Import the interface class
import Screen1

class ImageViewer(QtGui.QMainWindow, Screen1.Ui_MainWindow):
    """ The second parent must be 'Ui_<obj. name of main widget class>'.
    If confusing, simply open up ImageViewer.py and get the class
    name used. I'd named mine as mainWindow, hence Ui_mainWindow. """

    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        # This is because Python does not automatically
        # call the parent's constructor.
        self.setupUi(self)
        # Pass this "self" for building widgets and
        # keeping a reference.

    def main(self):
        self.show()

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.main()
    app.exec_()
      # This shows the interface we just created. No logic has been added, yet.
