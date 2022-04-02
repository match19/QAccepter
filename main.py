
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QWidget, QMainWindow, QLabel
from PyQt6 import uic


class App(QWidget):
   def __init__(self):
      super().__init__()
      uic.loadUi('main.ui', self)
      self.load_buttons()
   
   def load_buttons(self):
      self.btnToggle.clicked.connect(self.testButtonClicked)
      print("loading buttons")
   
   def testButtonClicked(self):
      attrs = vars(self)
      if(self.lblState.text() == "paused"):
         self.lblState.setText("online")
      else:
         self.lblState.setText("paused")
      
      print(self.lblState.text())


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = App()
   window.show()
   sys.exit(app.exec())
