# ---------------------------- Import Libraries & Some Constants ------------------------------- #
import pandas as pd
from tkinter import *
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
WORDS_FILE = r"D:\Python Bootcamp\Day 31- Intermediate - Flash Card App Capstone Project\data\french_words.csv"
WORDS_TO_LEARN_FILE = r"D:\Python Bootcamp\Day 31- Intermediate - Flash Card App Capstone Project\data\words_to_learn.csv"

# ---------------------------- Dataset ------------------------------- #
try:
    if os.path.exists(WORDS_TO_LEARN_FILE):
        words = pd.read_csv(WORDS_TO_LEARN_FILE)
    else:
        words = pd.read_csv(WORDS_FILE)
    words_dataframe = words.to_dict(orient="records")
except FileNotFoundError:
    print("Error: File not found.")
    words_dataframe = []


# ---------------------------- Functions ------------------------------- #
def right_new_word():
    """Remove the current word if the user knows it and save the updated list."""
    global current_word
    if current_word in words_dataframe:
        words_dataframe.remove(current_word)
        pd.DataFrame(words_dataframe).to_csv(WORDS_TO_LEARN_FILE, index=False)
    select_new_word()


def wrong_new_word():
    """Skip the current word."""
    select_new_word()


def select_new_word():
    """Select a new random word and update the card to display it."""
    global current_word, is_french
    if words_dataframe:
        current_word = random.choice(words_dataframe)
        is_french = True
        canvas.itemconfig(canvas_image, image=card_front)
        language.config(text="French", fg="black", bg="white")
        word.config(text=current_word["French"], fg="black", bg="white")
        window.after(3000, flip_card)
    else:
        language.config(text="", fg="black", bg="#91c2af")
        word.config(text="All words learned!", fg="black", bg="#91c2af")
        right_button.config(state="disabled")
        wrong_button.config(state="disabled")


def flip_card():
    """Flip the card to display the English translation."""
    global is_french
    if is_french:
        canvas.itemconfig(canvas_image, image=card_back)
        language.config(text="English", fg="white", bg="#91c2af")
        word.config(text=current_word["English"], fg="white", bg="#91c2af")
        is_french = False


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Canvas
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back = PhotoImage(
    file=r"D:\Python Bootcamp\Day 31- Intermediate - Flash Card App Capstone Project\images\card_back.png"
)
card_front = PhotoImage(
    file=r"D:\Python Bootcamp\Day 31- Intermediate - Flash Card App Capstone Project\images\card_front.png"
)
right = PhotoImage(
    file=r"D:\Python Bootcamp\Day 31- Intermediate - Flash Card App Capstone Project\images\right.png"
)
wrong = PhotoImage(
    file=r"D:\Python Bootcamp\Day 31- Intermediate - Flash Card App Capstone Project\images\wrong.png"
)

# Card image
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_button = Button(image=right, highlightthickness=0, command=right_new_word)
right_button.grid(column=1, row=1)

wrong_button = Button(image=wrong, highlightthickness=0, command=wrong_new_word)
wrong_button.grid(column=0, row=1)

# Labels
language = Label(text="French", font=("Arial", 40, "italic"), bg="white")
language.place(relx=0.5, rely=0.2, anchor="center")

word = Label(font=("Arial", 60, "bold"), bg="white")
word.place(relx=0.5, rely=0.5, anchor="center")

# Initialize the first word
current_word = {}
is_french = True
select_new_word()

# Run the application
window.mainloop()
