# implementation of card game - Memory

import simplegui
import random

turns = 0
# helper function to initialize globals
def new_game():
    global dock, exposed, state, turns
    turns = 0
    state = 0
    cards = range(0,8) * 2
    dock = []
    for card in cards:
        dock.append(card)
    random.shuffle(dock)
    exposed = [False] * 16
    label.set_text("Turns = " + str(turns))
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, turns, exposed, dock, clicked1, clicked2
    click = int(pos[0] / 50)
    if state == 0:
        state = 1
        clicked1 = click
        exposed[clicked1] = True
    elif state == 1:
        if not exposed[click]:
            state = 2
            clicked2 = click
            exposed[clicked2] = True
            turns += 1
    else:
        if not exposed[click]:
            if dock[clicked1] == dock[clicked2]: 
                exposed[clicked1] = True
                exposed[clicked2] = True
            else:
                exposed[clicked1] = False
                exposed[clicked2] = False
            clicked1 = click
            exposed[clicked1] = True
            state = 1
            label.set_text("Turns = " + str(turns)) 
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card in range(len(dock)):
        if exposed[card]: #if True draw number
            canvas.draw_text(str(dock[card]),(card * 50 + 10, 65), 48, 'White', "sans-serif")
        else: # draw green card
            canvas.draw_polygon([(50*card, 0), (50*card + 50, 0), (50*card + 50, 100), (50*card, 100)], 2, "Tomato", "SeaGreen")
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric