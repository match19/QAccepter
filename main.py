
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QWidget, QMainWindow, QLabel, QPushButton
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from classes.QAccepter import QAccepter
import os

class App(QWidget):
   lblState: QLabel
   btnToggle: QPushButton
   stateColor = {
      "paused": "background-color: rgb(206, 0, 3);",
      "default": "background-color: rgb(0, 255, 0);"
   }

   def __init__(self):
      super().__init__()
      dir_path = os.path.dirname(os.path.realpath(__file__))
      uic.loadUi(dir_path+'\\main.ui', self)
      self.load_buttons()
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.updateUI)
      self.timer.start(200)
      self.qaccepter = QAccepter()
      self.qaccepter.start()
   
   def updateUI(self):
      self.lblState.setText(str(self.qaccepter.get_state()))

   def load_buttons(self):
      self.btnToggle.clicked.connect(self.togglePause)
   
   def togglePause(self):
      if(self.qaccepter.get_state() == "paused"):
         self.qaccepter.start()
      else:
         self.qaccepter.pause()
   
if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = App()
   window.show()
   sys.exit(app.exec())
