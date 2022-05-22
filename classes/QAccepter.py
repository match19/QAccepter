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
            w = pygetwindow.getWindowsWithTitle("League of Legends")
            if len(w) != 0:
                w = w[0]
            else:
                w = None
            if("League of Legends (TM) Client" in apps and not self.__paused):
                self.__state = "ingame"
                time.sleep(2)
            elif("League of Legends" in apps and not self.__paused):
                if self.__state == "select":
                    if not QAccepter.userActive and self.ban_champ != "" and findLocation("ban", w):
                        select_champ(self.ban_champ, w)
                        click_lockin_or_ban(w)
                    elif not QAccepter.userActive and self.pick_champ != "" and findLocation("lockin", w):
                        select_champ(self.pick_champ, w)
                        self.__state = "lockin"
                    else:
                        self.__state = "online"
                elif self.__state == "lockin" and not QAccepter.userActive:
                    click_lockin_or_ban(w)
                    time.sleep(1)
                    if findLocation("lockin", w) == None:
                        self.__state = "online"
                elif not QAccepter.userActive and findLocation("search_champ", w):
                    self.__state = "select"
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

def select_champ(champ: str, w: pygetwindow.Win32Window):
    if not isinstance(w, pygetwindow.Win32Window):
        return
    click_search(w)
    ctrl_a_delete()
    pyautogui.write(champ)
    time.sleep(1)
    click_champ(w)

def click_champ(w: pygetwindow.Win32Window):
    if not isinstance(w, pygetwindow.Win32Window):
        return
    pyautogui.click(w.left + 390 * w.width/1280, w.top + 165 * w.height/720, 2)

def click_search(w: pygetwindow.Win32Window):
    if not isinstance(w, pygetwindow.Win32Window):
        return
    pyautogui.click(w.left + 820 * w.width/1280, w.top + 100 * w.height/720, 2)  # click search

def click_lockin_or_ban(w: pygetwindow.Win32Window):
    if not isinstance(w, pygetwindow.Win32Window):
        return
    pyautogui.click(w.left + 640 * w.width/1280, w.top + 602 * w.height/720, 2) #click ban


def ctrl_a_delete():
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("a")
    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("a")
    pyautogui.keyDown("delete")
    pyautogui.keyUp("delete")
   
