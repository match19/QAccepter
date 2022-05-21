from typing import Tuple
from PIL import ImageGrab
from win32api import GetSystemMetrics
import pyautogui
import pygetwindow
import time
import numpy as np
import threading
import cv2
from classes.action import *


def __findLocaction(filename: str) -> Tuple[int, int, int, int]:
    """Finds image from action/ folder in screenshot and returns location of image (x,y,width,height)"""
    fp = get_action_file(filename)
    # Make sure league window is active
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


def __clickLocation(filename: str) -> bool:
    loc = __findLocaction(filename)
    if(loc != None):
        x, y, width, height = loc
        w = pygetwindow.getWindowsWithTitle('League of Legends')[0]
        pyautogui.click(w.left+x+width/2, w.top+y+height/2, 2)
        return True
    return False


s = pygetwindow.getWindowsWithTitle('League of Legends')[0]
s = pygetwindow.getActiveWindowTitle()
# s = __clickLocation("search_champ")
# s = __findLocaction("play")
print(s)