from tkinter import *
import pandas
import random
from gtts import gTTS
import os

BACKGROUND_COLOR = "#B1DDC6"
my_timer = 0
current_card = {}
to_learn = {}

# Function to speak the Norwegian text
def speak_norwegian(text):
    tts = gTTS(text=text, lang='no')
    tts.save("norwegian_audio.mp3")  # Save the speech to an audio file
    os.system("afplay norwegian_audio.mp3")  # Play the audio file (MacOS)


# ---------------------------- functions ------------------------------- #

def next_click():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas_f.itemconfig(card_title, text="Norwegian", fill='green')
    canvas_f.itemconfig(card_word, text=current_card["Norwegian"], fill='green')
    canvas_f.itemconfig(front_image, image=my_fimage)
    # Speak the Norwegian text
    speak_norwegian(current_card["Norwegian"])
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas_f.itemconfig(front_image, image=my_bkimage)
    canvas_f.itemconfig(card_title, text="English", fill="white")
    canvas_f.itemconfig(card_word, text=current_card["English"], fill="white")

def save_remove():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_click()

# ---------------------------- Getting words ------------------------------- #

try:
    file_path = "./data/words_to_learn.csv"
    data = pandas.read_csv(file_path)
except FileNotFoundError:
    og_data = pandas.read_csv("data/NO_lang.csv")
    to_learn = og_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Learn Norwegian")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR, width=1000, height=1000)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, highlightthickness=0)

# backgrounds canvas
my_fimage = PhotoImage(file="./images/card_front.png")
canvas_f = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
front_image = canvas_f.create_image(400, 260, image=my_fimage)
card_title = canvas_f.create_text(400, 150, text="Norwegian", font=("Arial", 40, "italic"), fill="blue")
card_word = canvas_f.create_text(400, 300, text="", font=("Arial", 40, "italic"), fill="blue")
canvas_f.grid(column=1, row=1, columnspan=3)

my_bkimage = PhotoImage(file="./images/card_back.png")

next_click()

# Buttons
button_Rimage = PhotoImage(file="./images/right.png")
button_f = Button(image=button_Rimage, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=save_remove)
button_f.grid(column=3, row=3)

button_Wimage = PhotoImage(file="./images/wrong.png")
button_b = Button(image=button_Wimage, highlightthickness=0, highlightbackground=BACKGROUND_COLOR, command=next_click)
button_b.grid(column=1, row=3)

window.mainloop()
