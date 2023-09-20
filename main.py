import tkinter as t
from tkinter import messagebox
from random import randint, choice
import tkmacosx
import pandas as pd
import time
import os

# -------------------------- CONSTANTS, GLOBAL VARIABLE DECLARATIONS -------------------------- #

# Label font type
TITLE_FONT_NAME = 'American Typewriter'
FONT_NAME = 'American Typewriter'

# Label and Entry font color
LABEL_FONT_COLOR = '#402011'
LABEL_BACK_FONT_COLOR = '#ffffff'
# BTN_PRESSED_STATE = '#7F8C65'

# ORIGINAL_BACKGROUND_COLOR = "#B1DDC6"
BACKGROUNDS = ["#ffffff", "#D0E382", "#97993F", "#62D2C2", "#AFA6D0", "#8EABD2", "#AEB7A3", "#8F9FA1",
               "#CFCDBA", "#AB96A5", "#A89495", "#90A9B1", "#9CAB9C", "#9EB960", "#AFABA1", "#908E86",
               "#E9D5D2", "#DAAC2F", "#6D8665", "#AABBC4", "#7F8C65", "#8E939F", "#90A635", "#5F9386",
               "#66869C", "#CD9BB6", "#89748C", "#9C8CA9", "#A58EA4", "#B38496", "#C6C9CA", "#99928F",
               "#9C8D8A", "#AEC3B5", "#999D8D", "#889089", "#6B6963", "#627180", "#CAB8C4", "#D2D25C",
               "#B7B740"]

BACKGROUND_IMAGES_MAX_NR = 41
HIT_RANGES = [1, 8, 8]
MISS_RANGES = [1, 4, 4]

TITLE_FONT_SIZE = 30

MAX_TERM_FONT_SIZE = 50
MEDIUM_TERM_FONT_SIZE = 30
MIN_TERM_FONT_SIZE = 22

MAX_DEFINITION_FONT_SIZE = 45
MEDIUM_DEFINITION_FONT_SIZE = 30
MIN_DEFINITION_FONT_SIZE = 20

MAX_NOTES_FONT_SIZE = 30
MEDIUM_NOTES_FONT_SIZE = 20
MIN_NOTES_FONT_SIZE = 16

TITLE_YCOR = 100

TERM_YCOR_TOP = 180
TERM_YCOR_MEDIUM = 220
TERM_YCOR_BOTTOM = 250

DEFINITION_YCOR_TOP = 180
DEFINITION_YCOR_MEDIUM = 220
DEFINITION_YCOR_BOTTOM = 250

NOTES_YCOR_TOP = 290
NOTES_YCOR_UPPER_MEDIUM = 340
NOTES_YCOR_LOWER_MEDIUM = 380
NOTES_YCOR_BOTTOM = 420

random_color = ""
random_image = ""
random_hit_image = ""
random_hit_active_image = ""
random_miss_image = ""
random_miss_active_image = ""
language_switcher_image = ""


# -------------------------- DATA MANAGEMENT -------------------------- #


def set_learnset():
    data = pd.read_csv("data/own_dict.csv")
    to_learn = data.to_dict(orient='records')
    data_to_dump = pd.DataFrame(to_learn)
    data_to_dump.to_csv("data/learn_set.csv")


def reset_learnset():
    os.remove('data/learn_set.csv')
    set_learnset()


# First run / active learn set doesn't exists
try:
    try:
        print("first run")
        data = pd.read_csv("data/learn_set.csv")
    except FileNotFoundError:
        set_learnset()
    else:
        raise ValueError

# Active learn set is empty after running
except ValueError:
    reset_learnset()
else:
    pass
finally:
    data = pd.read_csv("data/learn_set.csv")
    # DataFrame hold bool values, True if the value is NaN
    isnull_data = data.isnull()
    to_learn = data.to_dict(orient='records')
    isnull_learn = isnull_data.to_dict(orient='records')

current_card = {}
current_card_isnull = {}
index = 0


# Calculate the next current card
def change_current_card_data():
    global index, current_card, current_card_isnull, to_learn, isnull_data, isnull_learn
    global index, current_card, current_card_isnull, to_learn, isnull_learn

    try:
        index = randint(1, len(to_learn) - 1)
        current_card = to_learn[index]
        current_card_isnull = isnull_learn[index]
    # All words learned case, miss button pressed
    except IndexError:
        print("IndexError in change_current_card_data")
        msg_box = t.messagebox.askquestion('Warning1', 'You reached the last word to learn. \nDo you want to restart?'
                                                       'Otherwise the program quit.', icon='warning')
        # If the user doesn't want to restart, exit
        if msg_box == 'no':
            root.destroy()
        if msg_box == 'yes':
            reset_learnset()

            data = pd.read_csv("data/learn_set.csv")
            to_learn = data.to_dict(orient='records')
            isnull_data = data.isnull()
            isnull_learn = isnull_data.to_dict(orient='records')

            index = randint(1, len(to_learn) - 1)
            current_card = to_learn[index]
            current_card_isnull = isnull_learn[index]
            to_learn.pop(index)
            isnull_learn.pop(index)
    else:
        pass


def change_learn_set():
    global to_learn, isnull_learn

    try:
        to_learn.pop(index)
        isnull_learn.pop(index)
    # All words learned case, hit button pressed
    except IndexError:
        print("IndexError in change_current_card_data")
        msg_box = t.messagebox.askquestion('Warning2', 'You reached the last word to learn. \nDo you want to restart?'
                                                       'Otherwise the program quit.', icon='warning')
        # If the user doesn't want to restart, exit
        if msg_box == 'no':
            root.destroy()
        if msg_box == 'yes':
            print("IndexError in change_learn_set")
            reset_learnset()

            data = pd.read_csv("data/learn_set.csv")
            to_learn = data.to_dict(orient='records')
            isnull_data = data.isnull()
            isnull_learn = isnull_data.to_dict(orient='records')
    else:
        data_to_dump = pd.DataFrame(to_learn)
        data_to_dump.to_csv("data/learn_set.csv")


# For the UI settings, first set a non NaN card
change_current_card_data()


# ------------------------------------------------------------------- #

# -------------------------- GUI FUNCTIONS -------------------------- #

# ------------------------------------------------------------------- #


# -------------------------- SET ELEMENTS -------------------------- #

# Calculate the random background, main images and the button pairs on every card change

def change_gui_elements():
    global random_color, random_image, random_hit_image, random_hit_active_image, random_miss_image, \
        random_miss_active_image
    random_bg_nr = randint(1, BACKGROUND_IMAGES_MAX_NR - 1)
    random_hit_nr = randint(1, HIT_RANGES[-1])

    random_image = "img/bg/bg " + str(random_bg_nr) + ".png"
    random_color = BACKGROUNDS[random_bg_nr]

    random_hit_img_nr_str = str(random_hit_nr)
    random_hit_image = "img/hit/hit " + random_hit_img_nr_str + ".png"
    random_hit_active_image = "img/hit/hit " + random_hit_img_nr_str + "a.png"
    random_miss_image = ""
    random_miss_active_image = ""

    #  Miss images are related hit images, we want to use random color in the same type group
    #  Number of files of hit and miss images in the same type group are different

    # For the case, we add more image groups later
    i = 0
    if random_hit_nr == HIT_RANGES[len(HIT_RANGES) - 1]:
        random_miss_image = "img/miss/miss " + str(MISS_RANGES[-1]) + ".png"
        random_miss_active_image = "img/miss/miss " + str(MISS_RANGES[-1]) + "a.png"
    while i < len(HIT_RANGES) - 1:
        if HIT_RANGES[i] <= random_hit_nr < HIT_RANGES[i + 1]:
            if HIT_RANGES[i] <= random_hit_nr < HIT_RANGES[i + 1]:
                random_miss_img_nr_str = str(randint(MISS_RANGES[i], MISS_RANGES[i + 1] - 1))
                random_miss_image = "img/miss/miss " + random_miss_img_nr_str + ".png"
                random_miss_active_image = ("img/miss/miss " + random_miss_img_nr_str + "a.png")
        i += 1

    # full random style: random color, random type
    # random_miss_image = "img/miss/miss " + str(randint(1, 20)) + ".png"
    return (random_color, random_image, random_hit_image, random_hit_active_image, random_miss_image,
            random_miss_active_image)


# -------------------------- CHANGE GUI -------------------------- #

# Set the above calculated UI elements
def change_gui():
    global random_color, bg_img, hit_img, hit_act_img, miss_img, miss_act_img

    change_gui_elements()
    root.config(bg=random_color)
    title.config(background=random_color)
    sub_title.config(background=random_color)
    canvas.config(bg=random_color)

    bg_img = t.PhotoImage(file=random_image)

    hit_img = t.PhotoImage(file=random_hit_image)
    hit_act_img = t.PhotoImage(file=random_hit_active_image)

    miss_img = t.PhotoImage(file=random_miss_image)
    miss_act_img = t.PhotoImage(file=random_miss_active_image)

    btn_hit.configure(image=hit_img, background=random_color, activeimage=hit_act_img, activebackground=random_color)
    btn_miss.configure(image=miss_img, background=random_color, activeimage=miss_act_img, activebackground=random_color)


# -------------------------- CHANGE CANVAS TEXT SIZE & POSITION -------------------------- #

def set_front_side_forth():
    if direction == 1:
        content = current_card["Term"]
    else:
        content = current_card["Definition"]

    if current_card_isnull['Notes, Examples']:
        if len(content) <= 32 and direction == 1:
            canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        elif len(content) <= 200 and direction == 1:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        elif len(content) > 200 and direction == 1:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_BOTTOM)

    elif len(current_card["Notes, Examples"]) <= 60:
        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, ''))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
        if len(content) <= 32:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        elif len(content) < 200:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        else:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

    elif len(current_card["Notes, Examples"]) <= 250:
        canvas.itemconfig(card_notes, font=(FONT_NAME, MEDIUM_NOTES_FONT_SIZE, ''))
        canvas.coords(card_notes, 400, NOTES_YCOR_UPPER_MEDIUM)
        if len(content) <= 32:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        elif len(content) < 200:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        else:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

    elif len(current_card["Notes, Examples"]) > 250:
        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, ''))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
        if len(content) <= 32:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)
        elif len(content) < 200:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        else:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)


def set_back_side_forth():
    if direction == 1:
        content = current_card["Definition"]
    else:
        content = current_card["Term"]

    if len(content) <= 32:
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, ''))
        canvas.coords(card_content, 400, DEFINITION_YCOR_BOTTOM)
    elif len(content) < 400:
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_DEFINITION_FONT_SIZE, ''))
        canvas.coords(card_content, 400, DEFINITION_YCOR_BOTTOM)
    else:
        canvas.itemconfig(card_content, font=(FONT_NAME, MIN_DEFINITION_FONT_SIZE, ''))
        canvas.coords(card_content, 400, DEFINITION_YCOR_BOTTOM)


def set_text_size_and_position(side):
    canvas.itemconfig(card_title, font=(TITLE_FONT_NAME, TITLE_FONT_SIZE, ''))
    canvas.coords(card_title, 400, TITLE_YCOR)

    if side == 1:
        set_front_side_forth()
    else:
        set_back_side_forth()


# ---------------------------------------------------------------- #

# -------------------------- Functions -------------------------- #

# ---------------------------------------------------------------- #


# -------------------------- FLIP CARD -------------------------- #


def flip_card(p=""):
    print(f'The direction is: {direction}')
    global current_card
    canvas.itemconfig(card_notes, text="")
    canvas.itemconfig(canvas_image, image=bg_img)

    if direction == 1:
        canvas.itemconfig(card_title, text="Definíció", fill='white',
                          font=(FONT_NAME, TITLE_FONT_SIZE, "bold"))
        canvas.itemconfig(card_content, text=current_card['Definition'], fill='white')

    else:
        canvas.itemconfig(card_title, text="Definition", fill='white',
                          font=(FONT_NAME, TITLE_FONT_SIZE, "normal"))
        canvas.itemconfig(card_content, text=current_card['Term'], fill='white')

    set_text_size_and_position(-1)


# -------------------------- NEXT CARD -------------------------- #


def next_card():
    global current_card, flip_timer
    canvas.itemconfig(canvas_image, image=fg_img)

    try:
        root.after_cancel(flip_timer)
    except NameError:
        pass
    else:
        pass

    change_current_card_data()

    if direction == 1:
        canvas.itemconfig(card_title, text="Term in Foreign Language")
        canvas.itemconfig(card_content, text=current_card['Term'], fill=LABEL_FONT_COLOR)

        if current_card_isnull['Notes, Examples']:
            canvas.itemconfig(card_notes, text="", fill=LABEL_FONT_COLOR)
        else:
            canvas.itemconfig(card_notes, text=current_card['Notes, Examples'], fill=LABEL_FONT_COLOR)

    else:
        canvas.itemconfig(card_title, text="Term in Native Language", fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_content, text=current_card['Definition'], fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_notes, text="")

    change_gui()
    set_text_size_and_position(1)

    flip_timer = root.after(6000, func=flip_card)


# -------------------------- KNOWN CARD -------------------------- #


def known_card(p=""):
    change_learn_set()
    next_card()


# -------------------------- SET DIRECTION -------------------------- #

# Direction of the translation (native <--> foreign language)
def set_direction(event):
    print("Set direction")
    global direction, language_switcher_image

    if direction == 1:
        canvas.itemconfig(lang_button_image, image=lang2_img)
        title.config(text="From Native to Foreign Language")
    else:
        canvas.itemconfig(lang_button_image, image=lang_img)
        title.config(text="From Foreign to Native Language")
    direction *= -1
    next_card()


def show_current(event):
    global current_card, flip_timer
    canvas.itemconfig(canvas_image, image=fg_img)

    root.after_cancel(flip_timer)

    if direction == 1:
        canvas.itemconfig(card_title, text="Term in Foreign Language")
        canvas.itemconfig(card_content, text=current_card['Term'], fill=LABEL_FONT_COLOR)

        if current_card_isnull['Notes, Examples']:
            canvas.itemconfig(card_notes, text="", fill=LABEL_FONT_COLOR)
        else:
            canvas.itemconfig(card_notes, text=current_card['Notes, Examples'], fill=LABEL_FONT_COLOR)

    else:
        canvas.itemconfig(card_title, text="Term in Native Language", fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_content, text=current_card['Definition'], fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_notes, text="")

    flip_timer = root.after(3000, func=flip_card)

    change_gui()
    set_text_size_and_position(1)


# ------------------------------------------------------------------- #

# -------------------------- GRID ELEMENTS -------------------------- #

# ------------------------------------------------------------------- #


root = t.Tk()
root.title("AnyLing")

change_gui_elements()

root.config(bg=random_color, padx=30)
root.config(width=1080, height=900)

direction = 1
title = t.Label(text="Practicing direction", foreground=LABEL_FONT_COLOR,
                background=random_color, font=("American TypeWriter", 30, ''), pady=20)
title.grid(row=0, column=0, columnspan=2)

sub_title = t.Label(text="(Click here to set up)", foreground=LABEL_FONT_COLOR,
                    background=random_color, font=("American TypeWriter", 20, ''))
sub_title.grid(row=1, column=0, columnspan=2)
sub_title.bind("<Button-1>", set_direction)

# -------------------------- CANVAS -------------------------- #

canvas = t.Canvas(width=800, height=526, bg=random_color, highlightthickness=0)

fg_img = t.PhotoImage(file="img/bg/bg 0.png")
bg_img = t.PhotoImage(file=random_image)

back_img = t.PhotoImage(file="img/back.png")
lang_img = t.PhotoImage(file="img/lang.png")
lang2_img = t.PhotoImage(file="img/lang2.png")

canvas_image = canvas.create_image(400, 264, image=fg_img)

card_title = canvas.create_text(400, 100, text="Title", font=(FONT_NAME, 30, ''), fill=LABEL_FONT_COLOR,
                                justify="left")
card_content = canvas.create_text(400, 200, text="Term", font=(FONT_NAME, 50, 'bold'), fill=LABEL_FONT_COLOR,
                                  justify="left", width=680)
card_notes = canvas.create_text(400, 350, text="Notes, Examples", font=(FONT_NAME, 30, 'italic'), fill=LABEL_FONT_COLOR,
                                justify="left", width=680)

back_button_image = canvas.create_image(50, 50, image=back_img)
lang_button_image = canvas.create_image(750, 50, image=lang_img)
canvas.grid(row=2, column=0, columnspan=2)

# -------------------------- BUTTONS -------------------------- #

hit_img = t.PhotoImage(file=random_hit_image)
hit_act_img = t.PhotoImage(file=random_hit_active_image)
btn_hit = tkmacosx.Button(image=hit_img, command=known_card, focuscolor='', background=random_color,
                          highlightthickness=0, borderless=1, activebackground=random_color)
btn_hit.grid(row=3, column=0)

miss_img = t.PhotoImage(file=random_miss_image)
miss_act_img = t.PhotoImage(file=random_miss_active_image)
btn_miss = tkmacosx.Button(image=miss_img, command=next_card, activeimage=miss_act_img, focuscolor='',
                           background=random_color, highlightthickness=0, borderless=1, activebackground=random_color)
btn_miss.grid(row=3, column=1)

# -------------------------- Logic -------------------------- #


next_card()
canvas.bind("<Button-1>", show_current)

root.mainloop()
