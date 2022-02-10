from imagesearch import *
from time import sleep
import pyautogui as pa

folder = "./image/"
DEBUG = True

def check_image(name, precision=0.7):
    pos = imagesearch(folder+name+".png", precision)
    if pos[0] != -1:
        if (DEBUG): print(name+" found : ", pos[0], pos[1])
        return pos
    else:
        return False

def search_click(name, precision=0.7, time=0.1):
        # Find button
        sleep(time*2)
        pos = imagesearch(folder+name+".png", precision)

        # Click button
        if pos[0] != -1:
            click_image(folder+name+".png", pos, "left", time)
            if (DEBUG): print(name+" button clicked")
            return True
        else:
            return False

def search_click_loop(name, precision=0.7, time=0.1, timeout=100):
        # Find button
        pos = imagesearch_loop_timeout(folder+name+".png", 0.2, precision=precision, timeout=timeout)

        # Click button
        if pos[0] != -1:
            click_image(folder+name+".png", pos, "left", time)
            if (DEBUG): print(name+" button clicked")

def wait_speedup_loop(trigger, coords, precision=0.7 , timeout=50, timesample=0.05, reverse=False, first_click=True, right_click=False):
    cancel = False
    rep = timeout
    img_search = isinstance(coords, str)

    while not cancel:
        if ((check_image(trigger, precision) != False) ^ reverse) or (rep <= 0):
            if (rep <= 0):
                print("Max timeout reached for "+trigger)
                return False
            cancel = True
        sleep(timesample)
        if img_search:
            if search_click(coords):
                if (first_click): cancel = True
        else:
            if (right_click):
                pa.rightClick(coords)
            else:
                pa.click(coords)
        if (DEBUG): print(rep)
        search_click("close", precision=0.7, time=0) #EVENT REPORTS
        rep = rep-1

    return True


def check_errors(coords):
    if (check_image("reboot") != False):
        search_click("reboot")
        search_click_loop("initiate")
        wait_speedup_loop("gate", coords)
        pa.click(coords)
        return True
    elif (check_image("retry", 0.9) != False):
        search_click("retry")
        sleep(5)
        return False
    else:
        return False