import random
from PIL import Image, ImageGrab
from win32api import GetSystemMetrics
import pyautogui
import pygetwindow
import time
import win32gui
import numpy as np
import threading
import pyglet
import cv2
from path import *

class QAccepter:
    def __init__(self):
        self.state = "ready"
        self.actionThread = None
        self.stateThread = None
        self.paused = True

    def start(self):
        self.paused = False
        self.stateThread = threading.Thread(target=self.__stateChecker, daemon=True)
        self.actionThread = threading.Thread(target=self.__doAction, daemon=True)
        self.stateThread.start()
        self.actionThread.start()
    
    def get_state(self):
        return self.state
    
    def pause(self):
        self.paused = True

    def __stateChecker(self):
        while(True and not self.paused):
            apps = pygetwindow.getAllTitles()
            if("League of Legends (TM) Client" in apps and not self.paused):
                self.state = "ingame"
                time.sleep(2)
                continue

            if("League of Legends" in apps and not self.paused):
                self.state = "online"
                time.sleep(2)
                continue
        self.state = "paused"

    def __doAction(self):
        while(True and not self.paused):
            if(self.state == "ingame" or self.state == ""):
                time.sleep(5)
                continue
            if(self.state == "online"):
                self.__clickLocation("accept")
                time.sleep(0.1)
                continue
            if(self.state == "lockinphase"):
                time.sleep(0.1)
                self.__lockinChamp()
                continue

    def __findLoc(self, filename):
        fp = path(filename)
        try:
            win = pygetwindow.getWindowsWithTitle('League of Legends')[0]
            if win.left < 0:
                raise Exception()
        except:
            return None

        dim = (win.left, win.top, win.left+win.width, win.top+win.height)
        img_rgb = ImageGrab.grab(bbox=dim)
        img_rgb = np.asarray(img_rgb)

        # Convert it to grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # Read the template
        template = cv2.imread(fp, 0)

        # Store width and height of template in w and h
        w, h = template.shape[::-1]

        # Perform match operations.
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # Specify a threshold
        threshold = 0.8

        # Store the coordinates of matched area in a numpy array
        loc = np.where(res >= threshold)
        retval = None
        try:
            retval = (loc[1][1], loc[0][0], w, h)
        except:
            pass
        return retval

    def __clickLocation(self, filename):
        loc = self.__findLoc(filename)
        if(loc != None):
            x, y, width, height = loc
            w = pygetwindow.getWindowsWithTitle('League of Legends')[0]
            pyautogui.click(w.left+x+width/2, w.top+y+height/2, 2)
            return True
        return False

    def __lockinChamp(self):
        if(self.__clickLocation("search")):
            pyautogui.write("kayle")
            time.sleep(0.2)
            self.__clickLocation("kayle")
            self.__clickLocation("lockin")
    

   
