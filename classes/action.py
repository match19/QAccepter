from typing import Tuple
from PIL import ImageGrab
import pyautogui
import pygetwindow
import numpy as np
import cv2
import os, fnmatch

def get_action_file(pattern):
    pattern = pattern + ".*"
    path = os.path.dirname(os.path.realpath(__file__))
    path = path + "/../action"
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return root+"/"+name

def findLocaction(filename: str, win: pygetwindow.Win32Window) -> Tuple[int, int, int, int]:
        """Finds image from action/ folder in screenshot and returns location of image (x,y,width,height)"""
        if(not isinstance(win, pygetwindow.Win32Window) or win.left < 0):
            return None

        fp = get_action_file(filename)
        if(fp == None):
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
        if len(loc[1]) < 2 or len(loc[0]) == 0:
            return None
       
        return (loc[1][1], loc[0][0], w, h)


def clickLocation(filename: str, win: pygetwindow.Win32Window) -> bool:
    loc = findLocaction(filename, win)
    if(loc != None):
        x, y, width, height = loc
        pyautogui.click(win.left+x+width/2, win.top+y+height/2, 2)
        return True
    return False