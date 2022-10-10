
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QWidget, QMainWindow, QLabel, QPushButton, QPlainTextEdit, QComboBox
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from classes.QAccepter import QAccepter
import os
import time

class App(QWidget):
   lblState: QLabel
   btnToggle: QPushButton
   pickChampDropdown: QComboBox
   banChampDropdown: QComboBox

   def __init__(self):
      super().__init__()
      dir_path = os.path.dirname(os.path.realpath(__file__))
      uic.loadUi(dir_path+'\\main.ui', self)
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.updateUI)
      self.timer.start(200)
      self.qaccepter = QAccepter()
      self.qaccepter.start()
      self.load_buttons()

   def mousePressEvent(self, e):
      self.setFocus()

   def updateUI(self):
      self.lblState.setText(str(self.qaccepter.get_state()))

   def load_buttons(self):
      self.btnToggle.clicked.connect(self.togglePause)
      for champ in self.qaccepter.champs:
         self.pickChampDropdown.addItem(champ)
         self.banChampDropdown.addItem(champ)
      self.pickChampDropdown.currentIndexChanged.connect(self.pick_changed)
      self.banChampDropdown.currentIndexChanged.connect(self.ban_changed)
   
   def pick_changed(self, i):
      self.qaccepter.pick_champ = self.pickChampDropdown.itemText(i)

   def ban_changed(self, i):
      self.qaccepter.ban_champ = self.pickChampDropdown.itemText(i)
   
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
