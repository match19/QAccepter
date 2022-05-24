from typing import Tuple
from PIL import  ImageGrab
from win32api import GetSystemMetrics
import pyautogui
import pygetwindow
import time
import threading
from pynput.mouse import Listener
from classes.action import *
from services.service_league import *

class QAccepter:
    #Check if user is active
    userActive = True
    lastActive = time.time()
    timeoutActive = 5

    def __init__(self):
        self.__state = "ready"
        self.__stateThread = None
        self.__paused = True
        self.pick_champ = ""
        self.ban_champ = ""
        self.champs = get_champs()

    def start(self):
        listener = Listener(on_move=on_move)
        listener.start()
        self.__state = "ready"
        self.__paused = False
        self.__stateThread = threading.Thread(target=self.__stateChecker, daemon=True)
        self.__stateThread.start()
    
    def pause(self):
        self.__paused = True

    def get_state(self):
        return self.__state
    
    def __checkUserActive(self):
        if time.time() - self.lastActive > QAccepter.timeoutActive:
            QAccepter.userActive = False

    def __stateChecker(self):
        while(True and not self.__paused):
            self.__checkUserActive()
            apps = pygetwindow.getAllTitles()
            w = get_lol_window()

            if("League of Legends (TM) Client" in apps and not self.__paused):
                self.__state = "ingame"
                time.sleep(5)
            elif("League of Legends" in apps and not self.__paused):
                if not QAccepter.userActive and self.pick_champ != "" and findLocation("lockin", w):
                    select_champ(self.pick_champ, w)
                    click_lockin_or_ban(w)
                elif not QAccepter.userActive and self.ban_champ != "" and findLocation("ban", w):
                    select_champ(self.ban_champ, w)
                    click_lockin_or_ban(w)
                else:
                    clickLocation("accept", w)
                    self.__state = "online"
                print(QAccepter.userActive, self.__state)
                time.sleep(2)
            else:
                time.sleep(3)

        self.__state = "paused"


def on_move(x, y):
   QAccepter.userActive = True
   QAccepter.lastActive = time.time()

def get_lol_window():
    w = pygetwindow.getWindowsWithTitle("League of Legends")
    if len(w) != 0 and w[0].left > 0:
        return w[0]
    else:
        return None