from imagesearch import *
from time import sleep
import pyautogui as pa
import pygetwindow as gw
from duel_utils import *

character = "tetsu"
duel_counter = 0
window = gw.getWindowsWithTitle("Yu-Gi-Oh! DUEL LINKS")[0]
event = "/quattro_event/"

x = window.left
y = window.top
w = window.width
h = window.height

draw_coords = (x+0.33*w, y+0.75*h)
chain_coords = (x+0.33*w, y+0.82*h)
next_coords = (x+0.5*w, y+0.92*h)
cards_coord = (x+0.465*w, y+0.9*h)
normal_summon_coords = (x+0.455*w, y+0.77*h)

enemy_monsters = [(x+0.44*w, y+0.36*h), (x+0.5*w,y+0.36*h), (x+0.56*w,y+0.36*h)] #left, middle, right
ally_monsters = [(x+0.5*w,y+0.58*h), (x+0.56*w,y+0.58*h), (x+0.44*w, y+0.58*h)] #middle, right, left

timeout = 0
print("Window at: ",x,y,"\nDimensions: ",h,w,"\n\n")
pyautogui.FAILSAFE = False

while True:
    # Entering the duel

    while check_image("auto_duel_on") == False:
        while not wait_speedup_loop(event+"quattro", event+"assist", 0.9, timeout=2, first_click=False) and timeout < 3:
            pa.scroll(-60)
            pa.click(draw_coords)
            pa.scroll(-100)
            pa.click(draw_coords)
            pa.scroll(-38)
            
#            if search_click(event+"assist_2", 0.9):
#                break
            if search_click("next", 0.9):
                pass
            if search_click("ok", 0.94):
                pass
            else:
                timeout = timeout + 1

        wait_speedup_loop("auto_duel", draw_coords, 0.9, timeout=6)

        wait_speedup_loop("auto_duel", "auto_duel", 0.97, timeout=5, first_click=True, reverse=True)
        sleep(0.6)

        if (check_image(event+"no_assist") != False) or check_image("auto_duel") != False:
            pa.click(draw_coords)
            pa.rightClick(draw_coords)
            sleep(0.2)

        if (check_image("reboot") != False):
            search_click("reboot")
            search_click_loop("initiate")
            dueling = False
            break
        elif (check_image("retry", 0.9) != False):
            search_click("retry")
            dueling = False
            break

    while not wait_speedup_loop("ok", "ok", 1, timesample=0.9, timeout=2) and timeout < 100:
        if (check_image(event+"rescue_complete")):
            wait_speedup_loop(event+"quattro", "back", 0.3)
            break
        else:
            timeout = timeout + 1
            if (check_image("reboot") != False):
                search_click("reboot")
                search_click_loop("initiate")
                dueling = False
                break
            elif (check_image("retry", 0.9) != False):
                search_click("retry")
                dueling = False
                break

    timeout = 0

    wait_speedup_loop(event+"end", next_coords, 0.9, timesample=0.1, timeout=45)
    pa.click(next_coords)

    search_click("ok")
    sleep(0.8)

    #Duel ends
    duel_counter = duel_counter + 1
    print("\t\nDuel Finished : "+str(duel_counter)+"\n")
