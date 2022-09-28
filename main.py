import random
import time
from tkinter import *
import pandas

# ---------------------------------- FUNCTIONALITY ---------------------------------- #

try:
    word_df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    word_df = pandas.read_csv("data/french_words.csv")
    to_learn = word_df.to_dict(orient="records")
else:
    to_learn = word_df.to_dict(orient="records")
finally:
    choice = None


def flip_card():
    global choice
    card_front.itemconfigure(card_img, image=card_back_img)
    card_front.itemconfigure(title_text, text="English", fill="white")
    card_front.itemconfigure(phrase_text, text=f"{choice['English']}", fill="white")


def random_word_pair():
    global choice, flip_timer
    window.after_cancel(flip_timer)
    card_front.itemconfigure(card_img, image=card_front_img)
    choice = random.choice(to_learn)
    card_front.itemconfigure(title_text, text="French", fill="black")
    card_front.itemconfigure(phrase_text, text=f"{choice['French']}", fill="black")
    flip_timer = window.after(3000, func=flip_card)


def remove_pair():
    global choice
    to_learn.remove(choice)
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    random_word_pair()

# ---------------------------------- UI SETUP ---------------------------------- #


BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(padx=34, pady=34, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
# ---------------------------------- CANVAS ---------------------------------- #

card_back_img = PhotoImage(file="images/card_back.png")

card_front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_img = card_front.create_image(400, 263, image=card_front_img)
title_text = card_front.create_text(400, 150, text="French", font=("Arial", 34, "italic"))
phrase_text = card_front.create_text(400, 263, text="Word", font=("Arial", 55, "bold"))
card_front.grid(row=0, column=0, columnspan=2)

random_word_pair()

# ---------------------------------- BUTTONS ---------------------------------- #

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, command=random_word_pair)
wrong_btn.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, command=remove_pair)
right_btn.grid(row=1, column=1)


window.mainloop()

