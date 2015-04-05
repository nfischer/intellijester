#!/usr/bin/python

from PyQt4 import QtGui, QtCore
import sys
import os
import api
import threading

import mp3

# Import the interface class
import Screen1
import Screen2
from JokeBag import JokeBag, JokeTooLong
from eeg import EEG
    

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
        while True:
            try:
                cat, joke = joke_bag.get_joke_wrapper()
                break
            except JokeTooLong as e:
                continue
        a = "CHECK"
        q = QtCore.QString(joke)
        self.textBrowser.setHtml(q)
        mp3.read_joke(joke)
        # Get user rating
        #val = -1
        #if eeg.user_likes_joke():
        #    print "He likes it!"
        #    val = 1
        #    self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("../assets/SadFaceSmall.png")))
        #else:
        #    print "He doesn't like it"
        #    self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("../assets/SadFaceSmall.png")))
        #joke_bag.change_score(next_cat, val)


    def handleButton(self):

        self.window1 = Screen1Main(self)
        self.window1.show()


def main():
    app = QtGui.QApplication(sys.argv)
    imageViewer = Screen1Main()
    imageViewer.main()
    app.exec_()


if __name__=='__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            usage()
            exit(0)

    global eeg
    # execute the main function now
    print "Initializing jokebag"
    global joke_bag
    joke_bag = JokeBag()
    global joke
    joke = ""
    eeg = EEG()
    print "Finished initialization"


    my_threads = list()
    my_threads.append(threading.Thread(target=eeg.listen_to_process) )
    my_threads.append(threading.Thread(target=main) )
    my_threads[0].daemon = True # run this thread in the background
    my_threads[1].daemon = False
    my_threads[0].start()
    my_threads[1].start()

    try:
        for t in my_threads:
            while t.isAlive():
                t.join(1)
    except:
        killProgram()

      # This shows the interface we just created. No logic has been added, yet.

def changeImage(happy):
    if happy == 1:
        print app.activeWindow()
    else:
        print "NOT"
    
        
