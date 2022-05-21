from typing import Tuple
from PIL import  ImageGrab
from win32api import GetSystemMetrics
import pyautogui
import pygetwindow
import time
import numpy as np
import threading
import cv2
from classes.action import *

class QAccepter:
    #Check if user is active
    userActive = False
    lastActive = 0
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
        self.actionThread = threading.Thread(target=self.__doAction, daemon=True)
        self.stateThread.start()
        self.actionThread.start()
    
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
            if("League of Legends (TM) Client" in apps and not self.paused):
                self.state = "ingame"
                time.sleep(2)
            elif("League of Legends" in apps and not self.paused):
                self.state = "online"
                time.sleep(2)
            else:
                time.sleep(3)

        self.state = "paused"

    def __doAction(self):
        while(True and not self.paused):
            if(self.state == "ingame" or self.state == "ready"):
                time.sleep(5)
            elif(self.state == "online"):
                w = pygetwindow.getWindowsWithTitle("League of Legends")
                if len(w) != 0:
                    w = w[0]
                    # clickLocation("accept", w)
                    if clickLocation("play", w):
                        time.sleep(5)
                time.sleep(0.2)
            else:
                time.sleep(5)

    def __lockinChamp(self):
        if(clickLocation("search", )):
            pyautogui.write("kayle")
            time.sleep(0.2)
            self.__clickLocation("kayle")
            self.__clickLocation("lockin")
    

   
