import pyautogui
import time
from classes.action import *
from pynput.mouse import Listener
import pygetwindow

w = pygetwindow.getWindowsWithTitle("League of Legends")[0]
print(w.left, w.top)
s = findLocaction("lockin", w)
print(s)
quit()


# pyautogui.click(640,602)
def on_move(x, y):
   print(x, y)


listener = Listener(on_move=on_move)
listener.start()

# time.sleep(50)
#640, 602

#1170, 730

#532 128 window corner
#search 1350, 230