
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QWidget, QMainWindow, QLabel
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from QAccepter import QAccepter


class App(QWidget):
   def __init__(self):
      super().__init__()
      uic.loadUi('main.ui', self)
      self.load_buttons()
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.update)
      self.timer.start(100)
      self.qaccepter = QAccepter()
      self.qaccepter.start()
   
   def update(self):
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
