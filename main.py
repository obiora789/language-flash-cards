from tkinter import *
import pandas
import random
from tkinter import messagebox

try:
    french_data = pandas.read_csv("./data/french_words_to_learn.csv")
    spanish_data = pandas.read_csv("/data/spanish_words_to_learn.csv")
except FileNotFoundError:
    french_data = pandas.read_csv("./data/french_english.csv")
    spanish_data = pandas.read_csv("./data/spanish_english.csv")

card_width = 800
card_height = 526
BACKGROUND_COLOR = "#B1DDC6"
ENGLISH_COLOR = "white"
LANGUAGE_COLOR = "black"
PADDING = 40
FONT_NAME = "Arial"
english_word = ""
language_word = ""
language_index = 0
front_language = ""
english = "English"
flip_to_english = False


def switch_to_english():
    """flips the card to display the english word. It also enables the buttons."""
    global flip_to_english
    flip_to_english = True
    card.itemconfig(front_id, image=back_img)
    card.itemconfig(lang_id, text=english, fill=ENGLISH_COLOR)
    card.itemconfig(word_id, text=english_word, fill=ENGLISH_COLOR)
    if flip_to_english:
        right_button.config(command=delete_items)
        wrong_button.config(command=reset)
    return flip_to_english


def reset():
    """flips the card to display the language word (Spanish or French). It also disables the buttons."""
    global flip_to_english
    manipulate_list()
    flip_to_english = False
    card.itemconfig(front_id, image=front_img)
    card.itemconfig(lang_id, text=front_language, fill=LANGUAGE_COLOR)
    card.itemconfig(word_id, text=language_word, fill=LANGUAGE_COLOR)
    window.after(3000, func=switch_to_english)
    if not flip_to_english:
        right_button.config(command="")
        wrong_button.config(command="")
    return flip_to_english


def manipulate_list():
    """gets the words from the data and updates the words_to_learn csv file"""
    global language_index, language_word, english_word, front_language
    choice_object = random.choice(language_dictionary)
    front_language = [key for key, _ in choice_object.items() if key == "French" or key == "Spanish"]
    front_language = front_language[0]
    language_index = language_dictionary.index(choice_object)
    language_word = choice_object[front_language]
    english_word = choice_object[english]
    write_data = pandas.DataFrame(language_dictionary)
    write_data.to_csv(f"./data/{front_language.lower()}_words_to_learn.csv", index=False)
    return language_index, front_language, language_word, english_word


def delete_items():
    """deletes known words from the list"""
    del language_dictionary[language_index]
    reset()


result = messagebox.askyesno(title="Choose Language", message="For French select 'Yes',"
                                                              " for Spanish, select 'No'.")
if result:
    language_dictionary = french_data.to_dict(orient="records")
else:
    language_dictionary = spanish_data.to_dict(orient="records")

window = Tk()
window.title("Language Cards")
window.config(padx=PADDING, pady=PADDING, background=BACKGROUND_COLOR, highlightthickness=0)

manipulate_list()

card = Canvas(width=card_width, height=card_height, highlightthickness=0, bg=BACKGROUND_COLOR)
back_img = PhotoImage(file="./images/card_back.png")
front_img = PhotoImage(file="./images/card_front.png")
front_id = card.create_image(card_width/2, card_height/2)
lang_id = card.create_text(card_width/2, card_height/3.5, fill="black", font=(FONT_NAME, 35, "italic"))
word_id = card.create_text(card_width/2, card_height/2, fill="black", font=(FONT_NAME, 50, "bold"))
card.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, border=0)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, border=0)
wrong_button.grid(row=1, column=0)
reset()

window.mainloop()
