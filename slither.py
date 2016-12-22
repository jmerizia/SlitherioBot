from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command

import time, math, base64, os
from bs4 import BeautifulSoup as BS4
from PIL import ImageGrab, Image

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None,
                    type,
                    (posx,posy),
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx, posy)

def mouseclick(posx,posy, t):
        # uncomment this line if you want to force the mouse
        # to MOVE to the click location first (I found it was not necessary).
        #mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx, posy)
        time.sleep(t)
        mouseEvent(kCGEventLeftMouseUp, posx, posy)

def deg2coord(deg):
    x_coord = 50 * math.cos(math.radians(deg))
    y_coord = 50 * math.sin(math.radians(deg))
    return x_coord, y_coord

def screencapture():
    os.system("screencapture -c -x")
    pic = ImageGrab.grabclipboard()
    pic = pic.crop((20, 100, 330, 410))
    return pic

## SETUP

x_center, y_center = 175, 255

driver = webdriver.Firefox()
driver.set_window_size(350, 390)
driver.set_window_position(0, 0)
driver.get("http://slither.io/")

name_elem = driver.find_element_by_id("nick")
name_elem.send_keys("jake", Keys.ENTER)
time.sleep(6) # put this value up if your internet is slow
# driver.execute_script("""
#     document.getElementsByClassName('nsi');
#     """)


## TRAINING

pic = screencapture()
pic.thumbnail((100, 100), Image.ANTIALIAS)
# print pic.size[0], pic.size[1]
pic.save("pic.png")

mouseclick(x_center, y_center, 0.001) # toggle window

soup = BS4(driver.page_source, "html.parser")
stuff = soup.html.body.contents[26].span.contents[1]
print stuff.get_text()

# Moves in a circle:
for deg in range(360):
    x_coord, y_coord = deg2coord(deg)
    mousemove(x_coord + x_center, y_coord + y_center)
    #mouseclick(x_coord + x_center, y_coord + y_center, 0.01)
    time.sleep(0.01)


driver.quit()
