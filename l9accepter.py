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

state = ""

def findLoc(filename):
    fp = path(filename)
    try:
        win = pygetwindow.getWindowsWithTitle('League of Legends')[0]
        if win.left < 0:
            raise Exception()
    except:
        return None

    dim = (win.left, win.top,win.left+win.width, win.top+win.height)
    img_rgb = ImageGrab.grab(bbox=dim)
    img_rgb = np.asarray(img_rgb)

    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    # Read the template
    template = cv2.imread(fp,0)
    
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.8
    
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    
    retval = None

    try:
        retval = (loc[1][1], loc[0][0], w, h)
    except:
        pass
    
    return retval


def clickLocation(filename):
    loc = findLoc( filename )
    if(loc != None):
        x, y, width, height  = loc
        w = pygetwindow.getWindowsWithTitle('League of Legends')[0]
        pyautogui.click(w.left+x+width/2, w.top+y+height/2, 2)
        return True
    return False

def stateChecker():
    global state
    while(True):
        apps = pygetwindow.getAllTitles()
        time.sleep(0.5)
        if("League of Legends" not in apps):
            state = ""
            time.sleep(2)
            continue

        if("League of Legends (TM) Client" in apps):
            state = "ingame"
            time.sleep(2)
            continue
        state = "online"

def lockinChamp():
    if(clickLocation("search")):
        pyautogui.write("kayle")
        time.sleep(0.2)
        clickLocation("kayle")
        clickLocation("lockin")

def main():
    global state
    while(True):
        time.sleep(0.1)
        if(state == "ingame" or state == ""):
            time.sleep(5)
            continue
        if(state == "online"):
            clickLocation("accept")
            continue
        if(state == "lockinphase"):
            lockinChamp()
            continue

        
actionThread = threading.Thread(target=main, daemon=True)
stateThread = threading.Thread(target=stateChecker, daemon=True)

actionThread.start()
stateThread.start()

win = pyglet.window.Window(width=400, height=400, caption = "L9 Q accepter")
label = pyglet.text.Label('Online',
                          font_name='Arial',
                          font_size=36,
                          x=win.width//2, y=win.height//2,
                          anchor_x='center', anchor_y='center')



def update(event):
    global state
    label.text = state
    win.clear()
    label.draw()


pyglet.clock.schedule_interval(update, .5)
pyglet.app.run()