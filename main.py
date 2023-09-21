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
# BACKGROUNDS = ["#ffffff", "#D0E382", "#97993F", "#62D2C2", "#AFA6D0", "#8EABD2", "#AEB7A3", "#8F9FA1",
#                "#CFCDBA", "#AB96A5", "#A89495", "#90A9B1", "#9CAB9C", "#9EB960", "#AFABA1", "#908E86",
#                "#E9D5D2", "#DAAC2F", "#6D8665", "#AABBC4", "#7F8C65", "#8E939F", "#90A635", "#5F9386",
#                "#66869C", "#CD9BB6", "#89748C", "#9C8CA9", "#A58EA4", "#B38496", "#C6C9CA", "#99928F",
#                "#9C8D8A", "#AEC3B5", "#999D8D", "#889089", "#6B6963", "#627180", "#CAB8C4", "#D2D25C",
#                "#B7B740"]

BACKGROUNDS = ["#ffffff", "#bdccd4", "#7d93aa", "#929d79", "#809778", "#c9b64c", "#c2c76c", "#596a63",
               "#70726c", "#5b7954", "#98995f", "#a7beae", "#77823c", "#81a2ac", "#bcc4b4", "#a794a9",
               "#c9c4b7", "#b8b7cc"]

BACKGROUND_IMAGES_MAX_NR = 11

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
hit_image = ""
miss_image = ""
language_switcher_image = ""
back_image = ""
refresh_image = ""
exit_image = ""


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
    global random_color, random_image
    random_bg_nr = randint(1, BACKGROUND_IMAGES_MAX_NR - 1)

    random_image = "img/bg/bg " + str(random_bg_nr) + ".png"
    random_color = BACKGROUNDS[random_bg_nr]

    return random_color, random_image


# -------------------------- CHANGE GUI -------------------------- #

# Set the above calculated UI elements
def change_gui():
    global random_color, bg_img, hit_image, miss_image, language_switcher_image, back_image, refresh_image, exit_image

    change_gui_elements()
    root.config(bg=random_color)
    title.config(background=random_color)
    sub_title.config(background=random_color)
    canvas.config(bg=random_color)

    bg_img = t.PhotoImage(file=random_image)

    hit_image = t.PhotoImage(file="img/hit.png")
    miss_image = t.PhotoImage(file="img/miss.png")
    language_switcher_image = t.PhotoImage(file="img/lang.png")
    back_image = t.PhotoImage(file="img/back.png")
    refresh_image = t.PhotoImage(file="img/refresh.png")
    exit_image = t.PhotoImage(file="img/exit.png")

    btn_hit.config(image=hit_image, background=random_color, activebackground=random_color)
    btn_miss.config(image=miss_image, background=random_color, activebackground=random_color)
    btn_language_switcher.config(image=language_switcher_image, background=random_color, activebackground=random_color)
    btn_back.config(image=back_image, background=random_color, activebackground=random_color)
    btn_refresh.config(image=refresh_image, background=random_color, activebackground=random_color)
    btn_exit.config(image=exit_image, background=random_color, activebackground=random_color)


# -------------------------- CHANGE CANVAS TEXT SIZE & POSITION -------------------------- #

def set_front_layout():
    print("Set front layout")

    if direction == 1:
        content = current_card["Term"]
    else:
        content = current_card["Definition"]

    if current_card_isnull['Notes, Examples']:
        if len(content) <= 36 and direction == 1:
            canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        elif len(content) <= 200 and direction == 1:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        elif len(content) > 200 and direction == 1:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_BOTTOM)

    elif len(current_card["Notes, Examples"]) <= 100:
        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, ''))
        canvas.coords(card_notes, 450, NOTES_YCOR_LOWER_MEDIUM)
        if len(content) <= 36:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        elif len(content) < 200:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        else:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)

    elif len(current_card["Notes, Examples"]) <= 320:
        canvas.itemconfig(card_notes, font=(FONT_NAME, MEDIUM_NOTES_FONT_SIZE, ''))
        canvas.coords(card_notes, 450, NOTES_YCOR_UPPER_MEDIUM)
        if len(content) <= 36:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        elif len(content) < 200:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        else:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)

    elif len(current_card["Notes, Examples"]) > 320:
        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, ''))
        canvas.coords(card_notes, 450, NOTES_YCOR_BOTTOM)
        if len(content) <= 36:
            canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)
        elif len(content) < 200:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)

        else:
            canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
            canvas.coords(card_content, 450, DEFINITION_YCOR_MEDIUM)


def set_back_layout():
    print("Set front layout")

    if direction == 1:
        content = current_card["Definition"]
    else:
        content = current_card["Term"]

    if len(content) <= 40:
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, ''))
        canvas.coords(card_content, 450, DEFINITION_YCOR_BOTTOM)
    elif len(content) < 400:
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_DEFINITION_FONT_SIZE, ''))
        canvas.coords(card_content, 450, DEFINITION_YCOR_BOTTOM)
    else:
        canvas.itemconfig(card_content, font=(FONT_NAME, MIN_DEFINITION_FONT_SIZE, ''))
        canvas.coords(card_content, 450, DEFINITION_YCOR_BOTTOM)


def set_text_size_and_position(side):
    print("Set layout")

    if side == 1:
        canvas.itemconfig(card_title, font=(TITLE_FONT_NAME, TITLE_FONT_SIZE, ''))
    canvas.coords(card_title, 450, TITLE_YCOR)

    if side == 1:
        set_front_layout()
    else:
        set_back_layout()


# ---------------------------------------------------------------- #

# -------------------------- Functions -------------------------- #

# ---------------------------------------------------------------- #


# -------------------------- FLIP CARD -------------------------- #


def flip_card():
    print(f'The direction is: {direction} - flip_card()')

    global current_card
    canvas.itemconfig(card_notes, text="")
    canvas.itemconfig(canvas_image, image=bg_img)

    if direction == 1:
        canvas.itemconfig(card_title, text="Definíció", fill='white', font=(FONT_NAME, TITLE_FONT_SIZE, "bold"))
        canvas.itemconfig(card_content, text=current_card['Definition'], fill='white')

    else:
        canvas.itemconfig(card_title, text="Definition", fill='white', font=(FONT_NAME, TITLE_FONT_SIZE, "bold"))
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
        canvas.itemconfig(card_title, text="Term in Foreign Language", fill=LABEL_FONT_COLOR)
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


def known_card():
    print(f'I knew!')

    change_learn_set()
    next_card()


# -------------------------- SET DIRECTION -------------------------- #

# Direction of the translation (native <--> foreign language)
def set_direction():
    print("Set direction")

    global direction, language_switcher_image

    if direction == 1:
        btn_language_switcher.config(image=native_language_image)
        title.config(text="From Native to Foreign Language")
    else:
        btn_language_switcher.config(image=foreign_language_image)
        title.config(text="From Foreign to Native Language")
    direction *= -1
    next_card()


def show_current():
    print(f'I show you)')

    global current_card, flip_timer
    canvas.itemconfig(canvas_image, image=fg_img)

    root.after_cancel(flip_timer)

    if direction == 1:
        canvas.itemconfig(card_title, text="Term in Foreign Language", fill=LABEL_FONT_COLOR)
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


def exit_app():
    root.destroy()


# ------------------------------------------------------------------- #

# -------------------------- GRID ELEMENTS -------------------------- #

# ------------------------------------------------------------------- #


root = t.Tk()
root.title("AnyLing")
root.config(padx=10, pady=20)

change_gui_elements()

root.config(bg=random_color, padx=30)
root.config()

direction = 1
title = t.Label(text="From Foreign to Native Language", foreground=LABEL_FONT_COLOR,
                background=random_color, font=("American TypeWriter", 30, ''), width=30)
title.grid(row=0, column=1, columnspan=2)

sub_title = t.Label(text="(Click to change)", foreground=LABEL_FONT_COLOR,
                    background=random_color, font=("American TypeWriter", 20, ''))
# sub_title.grid(row=1, column=1)
sub_title.grid(row=1, column=2)
sub_title.bind("<Button-1>", set_direction)

# -------------------------- CANVAS -------------------------- #

canvas = t.Canvas(width=900, height=526, bg=random_color, highlightthickness=0)

fg_img = t.PhotoImage(file="img/bg/bg 0.png")
bg_img = t.PhotoImage(file=random_image)

canvas_image = canvas.create_image(450, 264, image=fg_img)

card_title = canvas.create_text(450, 100, text="Term", font=(FONT_NAME, TITLE_FONT_SIZE, ''), fill=LABEL_FONT_COLOR,
                                justify="left")
card_content = canvas.create_text(450, 200, text="Term", font=(FONT_NAME, 50, 'bold'), fill=LABEL_FONT_COLOR,
                                  justify="left", width=800)
card_notes = canvas.create_text(450, 350, text="Notes, Examples", font=(FONT_NAME, 30, 'italic'), fill=LABEL_FONT_COLOR,
                                justify="left", width=800)
canvas.grid(row=2, column=0, columnspan=4)

# -------------------------- BUTTONS -------------------------- #

hit_image = t.PhotoImage(file="img/hit.png")
btn_hit = tkmacosx.Button(image=hit_image, command=known_card, focuscolor='', background=random_color,
                          highlightthickness=0, borderless=1, activebackground=random_color)
btn_hit.grid(row=3, column=1)

miss_img = t.PhotoImage(file="img/miss.png")
btn_miss = tkmacosx.Button(image=miss_image, command=next_card, focuscolor='',
                           background=random_color, highlightthickness=0, borderless=1, activebackground=random_color)
btn_miss.grid(row=3, column=2)

back_image = t.PhotoImage(file="img/back.png")
btn_back = tkmacosx.Button(image=back_image, command=show_current, focuscolor='', background=random_color,
                           highlightthickness=0, borderless=1, activebackground=random_color)
btn_back.grid(row=0, rowspan=2, column=0)

refresh_image = t.PhotoImage(file="img/refresh.png")
btn_refresh = tkmacosx.Button(image=refresh_image, command=reset_learnset, focuscolor='', background=random_color,
                              highlightthickness=0, borderless=1, activebackground=random_color)
btn_refresh.grid(row=3, column=0)

exit_image = t.PhotoImage(file="img/exit.png")
btn_exit = tkmacosx.Button(image=exit_image, command=exit_app, focuscolor='',
                           background=random_color, highlightthickness=0, borderless=1, activebackground=random_color)
btn_exit.grid(row=3, column=3)

foreign_language_image = t.PhotoImage(file="img/lang.png")
native_language_image = t.PhotoImage(file="img/lang2.png")
btn_language_switcher = tkmacosx.Button(image=foreign_language_image, command=set_direction, focuscolor='',
                                        background=random_color, highlightthickness=0, borderless=1,
                                        activebackground=random_color)
btn_language_switcher.grid(row=0, rowspan=2, column=3)

# -------------------------- Logic -------------------------- #


next_card()
change_gui()
flip_timer = root.after(1000000, func=flip_card)

root.mainloop()
