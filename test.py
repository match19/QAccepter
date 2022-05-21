import time
from classes.action import *
from pynput.mouse import Listener
# win = pygetwindow.getWindowsWithTitle('League of Legends')[0]
# s = clickLocation("search_champ", win)
# print(s)


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))


listener = Listener(on_move=on_move)

listener.start()

time.sleep(50)