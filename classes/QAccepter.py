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
    def __init__(self):
        self.state = "ready"
        self.actionThread = None
        self.stateThread = None
        self.paused = True
        self.debug = False

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
 
    def __stateChecker(self):
        while(True and not self.paused):
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
                self.__clickLocation("accept")
                time.sleep(0.2)
            else:
                time.sleep(5)

    def __findLocaction(self, filename: str) -> Tuple[int, int, int, int]:
        """Finds image from action/ folder in screenshot and returns location of image (x,y,width,height)"""
        fp = get_action_file(filename)
        #Make sure league window is active
        try:
            win = pygetwindow.getWindowsWithTitle('League of Legends')[0]
            if win.left < 0:
                return None
        except:
            return None
        # Take screenshot of League window
        dim = (win.left, win.top, win.left+win.width, win.top+win.height)
        img_rgb = ImageGrab.grab(bbox=dim)

        # img_rgb.save("temp.png") #Save image for debugging
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

    def __clickLocation(self, filename: str) -> bool:
        loc = self.__findLocaction(filename)
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
    

   
