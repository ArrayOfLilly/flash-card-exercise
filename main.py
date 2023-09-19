import tkinter as t
from random import randint, choice
import tkmacosx
import pandas as pd
import time

# -------------------------- CONSTANTS, GLOBAL VARIABLE DECLARATIONS -------------------------- #

# Label font type
TITLE_FONT_NAME = 'American Typewriter'
FONT_NAME = 'American Typewriter'

# Label and Entry font color
LABEL_FONT_COLOR = '#402011'
LABEL_BACK_FONT_COLOR = '#ffffff'
BTN_PRESSED_STATE = '#7F8C65'

# ORIGINAL_BACKGROUND_COLOR = "#B1DDC6"
BACKGROUNDS = ["#ffffff", "#D0E382", "#97993F", "#62D2C2", "#AFA6D0", "#8EABD2", "#AEB7A3", "#8F9FA1",
               "#CFCDBA", "#AB96A5", "#A89495", "#90A9B1", "#9CAB9C", "#9EB960", "#AFABA1", "#908E86",
               "#E9D5D2", "#DAAC2F", "#6D8665", "#AABBC4", "#7F8C65", "#8E939F", "#90A635", "#5F9386",
               "#66869C", "#CD9BB6", "#89748C", "#9C8CA9", "#A58EA4", "#B38496", "#C6C9CA", "#99928F",
               "#9C8D8A", "#AEC3B5", "#999D8D", "#889089", "#6B6963", "#627180", "#CAB8C4", "#D2D25C",
               "#B7B740"]

BACKGROUND_IMAGES_MAX_NR = 41
HIT_RANGES = [1, 8, 16, 16]
MISS_RANGES = [1, 4, 8, 8]

TITLE_FONT_SIZE = 26

MAX_TERM_FONT_SIZE = 60
MEDIUM_TERM_FONT_SIZE = 30
MIN_TERM_FONT_SIZE = 22

MAX_DEFINITION_FONT_SIZE = 50
MEDIUM_DEFINITION_FONT_SIZE = 30
MIN_DEFINITION_FONT_SIZE = 20

MAX_NOTES_FONT_SIZE = 30
MIN_NOTES_FONT_SIZE = 16

TITLE_YCOR = 100

TERM_YCOR_TOP = 180
TERM_YCOR_MEDIUM = 230
TERM_YCOR_BOTTOM = 260

DEFINITION_YCOR_TOP = 180
DEFINITION_YCOR_MEDIUM = 230
DEFINITION_YCOR_BOTTOM = 260

NOTES_YCOR_TOP = 270
NOTES_YCOR_UPPER_MEDIUM = 300
NOTES_YCOR_LOWER_MEDIUM = 350
NOTES_YCOR_BOTTOM = 380

random_color = ""
random_image = ""
random_hit_image = ""
random_hit_active_image = ""
random_miss_image = ""
random_miss_active_image = ""

# -------------------------- DATA MANAGEMENT -------------------------- #

# First run / active learn set doesn't exists
try:
    data = pd.read_csv("data/learn_set.csv")
except FileNotFoundError:
    data = pd.read_csv("data/own_dict.csv")
    to_learn = data.to_dict(orient='records')
    data_to_dump = pd.DataFrame(to_learn)
    data_to_dump.to_csv("data/learn_set.csv")
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

    try:
        index = randint(1, len(to_learn) - 1)

    # All words learned case
    except IndexError:
        new_data = pd.read_csv("data/own_dict.csv")
        new_data.to_csv("data/learn_set.csv")
        to_learn = new_data.to_dict(orient='records')

        isnull_data = new_data.isnull()
        isnull_learn = isnull_data.to_dict(orient='records')

        index = randint(1, len(to_learn) - 1)
    else:
        pass
    finally:
        current_card = to_learn[index]
        current_card_isnull = isnull_learn[index]


def change_learn_set():
    global to_learn, isnull_learn

    to_learn.pop(index)
    isnull_learn.pop(index)
    data_to_dump = pd.DataFrame(to_learn)
    data_to_dump.to_csv("data/learn_set.csv")


# For the UI settings, firs set a non NaN card
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
    if len(current_card["Term"]) <= 17 and current_card_isnull['Notes, Examples']:
        print("Case 1.1")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif len(current_card["Term"]) <= 17 and len(current_card["Notes, Examples"]) <= 35:
        print("Case 1.2")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif len(current_card["Term"]) <= 17 and 35 < len(current_card["Notes, Examples"]) <= 70:
        print("Case 1.3")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif len(current_card["Term"]) <= 17 and 70 < len(current_card["Notes, Examples"]):
        print("Case 1.4")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_TOP)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    # Same as CASE_1_1
    elif 17 < len(current_card["Term"]) <= 34 and current_card_isnull['Notes, Examples']:
        print("Case 2.1")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_BOTTOM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    # Same as CASE_1_1
    elif 17 < len(current_card["Term"]) <= 34 and len(current_card["Notes, Examples"]) <= 35:
        print("Case 2.2")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    # Same as CASE_1_2
    elif 17 < len(current_card["Term"]) <= 34 and 35 < len(current_card["Notes, Examples"]) <= 70:
        print("Case 2.3")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    elif 17 < len(current_card["Term"]) <= 34 and 70 < len(current_card["Notes, Examples"]):
        print("Case 2.4")
        canvas.itemconfig(card_content, font=(FONT_NAME, 50, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif 34 < len(current_card["Term"]) and current_card_isnull['Notes, Examples']:
        print("Case 3.1")
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_BOTTOM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    # Same as CASE_3_1
    elif 34 < len(current_card["Term"]) and len(current_card["Notes, Examples"]) <= 35:
        print("Case 3.2")
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    elif 34 < len(current_card["Term"]) and 35 < len(current_card["Notes, Examples"]) <= 70:
        print("Case 3.3")
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    elif 34 < len(current_card["Term"]) and 70 < len(current_card["Notes, Examples"]):
        print("Case 3.4")
        canvas.itemconfig(card_content, font=(FONT_NAME, MIN_TERM_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, TERM_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)


def set_back_side_forth():
    if len(current_card["DEFINITION"]) <= 17 and current_card_isnull['Notes, Examples']:
        print("Case 1.1")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif len(current_card["DEFINITION"]) <= 17 and len(current_card["Notes, Examples"]) <= 35:
        print("Case 1.2")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif len(current_card["DEFINITION"]) <= 17 and 35 < len(current_card["Notes, Examples"]) <= 70:
        print("Case 1.3")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif len(current_card["DEFINITION"]) <= 17 and 70 < len(current_card["Notes, Examples"]):
        print("Case 1.4")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_TOP)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    # Same as CASE_1_1
    elif 17 < len(current_card["DEFINITION"]) <= 34 and current_card_isnull['Notes, Examples']:
        print("Case 2.1")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_BOTTOM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    # Same as CASE_1_1
    elif 17 < len(current_card["DEFINITION"]) <= 34 and len(current_card["Notes, Examples"]) <= 35:
        print("Case 2.2")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    # Same as CASE_1_2
    elif 17 < len(current_card["DEFINITION"]) <= 34 and 35 < len(current_card["Notes, Examples"]) <= 70:
        print("Case 2.3")
        canvas.itemconfig(card_content, font=(FONT_NAME, MAX_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    elif 17 < len(current_card["DEFINITION"]) <= 34 and 70 < len(current_card["Notes, Examples"]):
        print("Case 2.4")
        canvas.itemconfig(card_content, font=(FONT_NAME, 50, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)
    elif 34 < len(current_card["DEFINITION"]) and current_card_isnull['Notes, Examples']:
        print("Case 3.1")
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_BOTTOM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    # Same as CASE_3_1
    elif 34 < len(current_card["DEFINITION"]) and len(current_card["Notes, Examples"]) <= 35:
        print("Case 3.2")
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MAX_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    elif 34 < len(current_card["DEFINITION"]) and 35 < len(current_card["Notes, Examples"]) <= 70:
        print("Case 3.3")
        canvas.itemconfig(card_content, font=(FONT_NAME, MEDIUM_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_BOTTOM)
    elif 34 < len(current_card["DEFINITION"]) and 70 < len(current_card["Notes, Examples"]):
        print("Case 3.4")
        canvas.itemconfig(card_content, font=(FONT_NAME, MIN_DEFINITION_FONT_SIZE, 'bold'))
        canvas.coords(card_content, 400, DEFINITION_YCOR_MEDIUM)

        canvas.itemconfig(card_notes, font=(FONT_NAME, MIN_NOTES_FONT_SIZE, 'italic'))
        canvas.coords(card_notes, 400, NOTES_YCOR_LOWER_MEDIUM)


def set_text_size_and_position(side):
    canvas.itemconfig(card_title, font=(TITLE_FONT_NAME, TITLE_FONT_SIZE, ''))
    canvas.coords(card_title, 400, 100)

    # From foreign language to native
    if direction == 1:
        # Front side
        if side == 1:
            set_front_side_forth()
        else:
            set_back_side_forth()

    # From native to foreign language
    if direction == -1:
        # Front side
        if side == 1:
            set_back_side_forth()
        else:
            set_front_side_forth()


# ---------------------------------------------------------------- #

# -------------------------- Functions -------------------------- #

# ---------------------------------------------------------------- #


# -------------------------- FLIP CARD -------------------------- #


def flip_card():
    global current_card
    canvas.itemconfig(card_notes, text="")
    canvas.itemconfig(canvas_image, image=bg_img)

    # Term is longer than 1 line, but not more than 2

    if direction == 1:
        canvas.itemconfig(card_title, text="Definíció", fill=LABEL_BACK_FONT_COLOR)
        canvas.itemconfig(card_content, text=current_card['Definition'], fill=LABEL_BACK_FONT_COLOR)

        # if 16 < len(current_card["Definition"]) > 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 290)
        #     canvas.coords(card_notes, 400, 350)
        # # Term is longer than 1 line, but not more than 2
        # elif len(current_card["Definition"]) >= 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 30, "bold"))
        #     canvas.coords(card_content, 400, 200)
        #     canvas.coords(card_notes, 400, 330)
        # # Term is 1 line long
        # else:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 180)
        #     canvas.coords(card_notes, 400, 280)

    else:
        canvas.itemconfig(card_title, text="Definition", fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_content, text=current_card['Term'], fill=LABEL_FONT_COLOR)

        # if 16 < len(current_card["Term"]) > 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 290)
        #     canvas.coords(card_notes, 400, 350)
        # # Term is longer than 1 line, but not more than 2
        # elif len(current_card["Term"]) >= 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 30, "bold"))
        #     canvas.coords(card_content, 400, 200)
        #     canvas.coords(card_notes, 400, 330)
        # # Term is 1 line long
        # else:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 180)
        #     canvas.coords(card_notes, 400, 280)

    set_text_size_and_position(-1)


# -------------------------- NEXT CARD -------------------------- #


def next_card():
    global current_card, flip_timer
    canvas.itemconfig(canvas_image, image=fg_img)

    root.after_cancel(flip_timer)

    change_current_card_data()

    if direction == 1:
        canvas.itemconfig(card_title, text="Term", fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_content, text=current_card['Term'], fill=LABEL_FONT_COLOR)

        # # print(len(current_card["Term"]))
        # # print(len(current_card['Notes, Examples']))
        #
        # # Term is longer than 1 line, but not more than 2
        # if 16 < len(current_card["Term"]) > 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 290)
        #     canvas.coords(card_notes, 400, 350)
        # # Term is longer than 1 line, but not more than 2
        # elif len(current_card["Term"]) >= 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 30, "bold"))
        #     canvas.coords(card_content, 400, 200)
        #     canvas.coords(card_notes, 400, 330)
        # # Term is 1 line long
        # else:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 180)
        #     canvas.coords(card_notes, 400, 280)

        if current_card_isnull['Notes, Examples']:
            canvas.itemconfig(card_notes, text="", fill=LABEL_FONT_COLOR)
            # canvas.coords(card_content, 400, 270)
            # canvas.coords(card_notes, 400, 330)
        else:
            canvas.itemconfig(card_notes, text=current_card['Notes, Examples'], fill=LABEL_FONT_COLOR)

    else:
        canvas.itemconfig(card_title, text="Term", fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_content, text=current_card['Definition'], fill=LABEL_FONT_COLOR)
        canvas.itemconfig(card_notes, text="")

        # if 16 < len(current_card["Definition"]) > 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 260)
        #     canvas.coords(card_notes, 400, 350)
        # # Term is longer than 1 line, but not more than 2
        # elif len(current_card["Definition"]) >= 32:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 30, "bold"))
        #     canvas.coords(card_content, 400, 260)
        #     canvas.coords(card_notes, 400, 350)
        # # Term is 1 line long
        # else:
        #     canvas.itemconfig(card_content, font=(FONT_NAME, 60, "bold"))
        #     canvas.coords(card_content, 400, 230)
        #     canvas.coords(card_notes, 400, 280)

    change_gui()
    set_text_size_and_position(1)

    flip_timer = root.after(3000, func=flip_card)


# -------------------------- KNOWN CARD -------------------------- #


def known_card():
    change_current_card_data()
    change_learn_set()
    next_card()


# -------------------------- SET DIRECTION -------------------------- #

# Direction of the translation (native <--> foreign language)
def set_direction(event):
    global direction, flip_timer

    root.after_cancel(flip_timer)

    if direction == 1:
        title.config(text="From English to Hungarian    (Click to change)")
        next_card()
    else:
        title.config(text="From Hungarian to English    (Click to change)")
        next_card()

    direction *= -1


# ------------------------------------------------------------------- #

# -------------------------- GRID ELEMENTS -------------------------- #

# ------------------------------------------------------------------- #


root = t.Tk()
root.title("AnyLing")

change_gui_elements()

root.config(bg=random_color, padx=30)
root.config(width=900, height=600)

flip_timer = root.after(5000, func=flip_card)

direction = 1
title = t.Label(text="From English to Hungarian (Click to change)", foreground=LABEL_FONT_COLOR,
                background=random_color,
                font=("American TypeWriter", 26, ''), pady=30)
title.bind("<Button-1>", set_direction)
title.grid(row=0, column=0, columnspan=2)

# -------------------------- CANVAS -------------------------- #

canvas = t.Canvas(width=800, height=527, bg=random_color, highlightthickness=0)
fg_img = t.PhotoImage(file="img/bg/bg 0.png")
bg_img = t.PhotoImage(file=random_image)
canvas_image = canvas.create_image(400, 264, image=fg_img)
card_title = canvas.create_text(400, 100, text="Title", font=("American TypeWriter", 26, ''), fill=LABEL_FONT_COLOR,
                                justify="left", width=660)
card_content = canvas.create_text(400, 200, text="Term", font=(FONT_NAME, 60, 'bold'), fill=LABEL_FONT_COLOR,
                                  justify="left", width=660)
card_notes = canvas.create_text(400, 350, text="Notes, Examples", font=(FONT_NAME, 30, 'italic'), fill=LABEL_FONT_COLOR,
                                justify="left", width=680)
canvas.grid(row=1, column=0, columnspan=2)

# -------------------------- BUTTONS -------------------------- #

hit_img = t.PhotoImage(file=random_hit_image)
hit_act_img = t.PhotoImage(file=random_hit_active_image)
btn_hit = tkmacosx.Button(image=hit_img, command=known_card, focuscolor='', background=random_color,
                          highlightthickness=0,
                          borderless=1, activebackground=random_color)
btn_hit.grid(row=2, column=0)

miss_img = t.PhotoImage(file=random_miss_image)
miss_act_img = t.PhotoImage(file=random_miss_active_image)
btn_miss = tkmacosx.Button(image=miss_img, command=next_card, activeimage=miss_act_img, focuscolor='',
                           background=random_color,
                           highlightthickness=0, borderless=1, activebackground=random_color)
btn_miss.grid(row=2, column=1)


# -------------------------- Logic -------------------------- #

next_card()

root.mainloop()
