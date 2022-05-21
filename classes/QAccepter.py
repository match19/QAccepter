from typing import Tuple
from PIL import  ImageGrab
from win32api import GetSystemMetrics
import pyautogui
import pygetwindow
import time
import threading
import cv2
from classes.action import *

class QAccepter:
    #Check if user is active
    userActive = True
    lastActive = time.time()
    timeoutActive = 5

    def __init__(self):
        self.state = "ready"
        self.actionThread = None
        self.stateThread = None
        self.paused = True

    def start(self):
        self.state = "ready"
        self.paused = False
        self.stateThread = threading.Thread(target=self.__stateChecker, daemon=True)
        self.stateThread.start()
    
    def pause(self):
        self.paused = True

    def get_state(self):
        return self.state
    
    def __checkUserActive(self):
        if time.time() - self.lastActive > QAccepter.timeoutActive:
            QAccepter.userActive = False

    def __stateChecker(self):
        while(True and not self.paused):
            self.__checkUserActive()
            apps = pygetwindow.getAllTitles()
            w = pygetwindow.getWindowsWithTitle("League of Legends")
            if len(w) != 0:
                w = w[0]
            else:
                w = None
            if("League of Legends (TM) Client" in apps and not self.paused):
                self.state = "ingame"
                time.sleep(2)
            elif("League of Legends" in apps and not self.paused):
                if self.state == "select":
                    if not QAccepter.userActive and findLocaction("ban", w):
                        click_search(w)
                        ctrl_a_delete()
                        pyautogui.write("garen")
                        time.sleep(1)
                        click_champ(w)
                        click_lockin_or_ban(w)
                    elif not QAccepter.userActive and findLocaction("lockin", w):
                        click_search(w)
                        ctrl_a_delete()
                        pyautogui.write("kayle")
                        time.sleep(1)
                        click_champ(w)
                        self.state = "lockin"
                    else:
                        self.state = "online"
                elif self.state == "lockin" and not QAccepter.userActive:
                    click_lockin_or_ban(w)
                    time.sleep(1)
                    if findLocaction("lockin", w) == None:
                        self.state = "online"
                elif not QAccepter.userActive and findLocaction("search_champ", w):
                    self.state = "select"
                else:
                    clickLocation("accept", w)
                    self.state = "online"
                print(QAccepter.userActive, self.state)
                time.sleep(2)
            else:
                time.sleep(3)

        self.state = "paused"


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
   
