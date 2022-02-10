from imagesearch import *
from time import sleep
import pyautogui as pa
import pygetwindow as gw
from duel_utils import *

pyautogui.FAILSAFE = False
duel_counter = 0
window = gw.getWindowsWithTitle("Yu-Gi-Oh! DUEL LINKS")[0]

x = window.left
y = window.top
w = window.width
h = window.height

portal_coords = (x+0.55*w, y+0.45*h)
draw_coords = (x+0.33*w, y+0.75*h)
chain_coords = (x+0.33*w, y+0.82*h)
next_coords = (x+0.5*w, y+0.92*h)
cards_coord = (x+0.465*w, y+0.9*h)
normal_summon_coords = (x+0.455*w, y+0.77*h)

enemy_monsters = [(x+0.44*w, y+0.36*h), (x+0.5*w,y+0.36*h), (x+0.56*w,y+0.36*h)] #left, middle, right
ally_monsters = [(x+0.5*w,y+0.58*h), (x+0.56*w,y+0.58*h), (x+0.44*w, y+0.58*h)] #middle, right, left

timeout = 0
print("Window at: ",x,y,"\nDimensions: ",h,w,"\n\n")
input()

while True:
    # Entering the duel

    while True or timeout < 10:
        if check_image("back") != False:
            search_click_loop("back", 1, 0.2, timeout=6)
            wait_speedup_loop("gate", "gate", 0.8, timeout=40, timesample=0.7, reverse=True)
            break
        if check_image("gate") != False:
            wait_speedup_loop("gate", "gate", 0.8, timeout=40, timesample=0.7, reverse=True)
            break
        else:
            timeout = timeout + 1

    wait_speedup_loop("duel", "duel", 0.8, timeout=20)
    # wait_speedup_loop("duel", "duel", 0.8, timeout=60, reverse=True)
    sleep(0.1)
    search_click("yes", 0.7, 0.2)
    wait_speedup_loop("duel", draw_coords, 0.8, timeout=20)
    wait_speedup_loop("duel", "duel", 1, 30, reverse=True)

    dueling = True
    skip = False
    turn = 0
    monsters = 0

    while dueling:
        print("\nMain phase ", "   Turn:  ", turn, "   Duel counter: ", duel_counter)
        if (check_image("reboot") != False):
            search_click("reboot")
            search_click_loop("initiate")
            dueling = False
            break
        if (check_image("retry", 0.9) != False):
            search_click("retry")
            dueling = False
            break

        # Speed up draw phase
        wait_speedup_loop("main_phase", draw_coords, 0.9, 100)
        imagesearch_loop_timeout(folder+"action.png", 0.1, 40)
        if monsters < 3:
            sleep(0.1)
            pa.click(cards_coord)
            if search_click("normal_summon", time=0.1):
                monsters = monsters + 1

        pa.click(draw_coords)
        search_click_loop("action")
        imagesearch_loop_timeout(folder+"end_phase.png", 0.1, 40)
        if (turn == 0 and check_image("battle_phase", precision=0.6) == False):
             search_click_loop("end_phase")
             turn = turn + 1
             skip = True
        else:
            search_click_loop("battle_phase", precision=0.6)
            sleep(0.1)
            for coords in ally_monsters[:monsters]:
                if (not dueling): break
                pa.click(coords)
                sleep(0.1)
                if (check_image("attack") != False):
                    search_click("attack")
                    sleep(0.2)
                    if check_image("enemy_monster_subimage"):
                        search_click_loop("enemy_monster_subimage", 0.8, timeout=1)
                        search_click("confirm_enabled", precision=0.7)
                    while timeout < 30:
                        if check_image("action") != False:
                            break
                        if check_image("ok", precision=0.7) != False:
                            dueling = False
                            break
                        timeout = timeout + 1
                else:
                    sleep(0.1)
            turn = turn + 1

        timeout = 0
        while timeout < 40 and dueling:
            if (check_image("ok") != False):
                dueling = False
                break
            if (check_image("action") != False):
                search_click_loop("action")
                search_click_loop("end_phase", 0.8)
                break
            if skip:
                skip = False
                break
            timeout = timeout + 1
        timeout = 0


    #Duel ends
    wait_speedup_loop("gate", next_coords, right_click=True)
    duel_counter = duel_counter + 1
    print("\t\nDuel Finished : "+str(duel_counter)+"\n")
