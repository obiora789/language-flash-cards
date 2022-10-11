from tkinter import *
import pandas
import random
from tkinter import messagebox

french_data = pandas.read_csv("./data/french_english.csv")
spanish_data = pandas.read_csv("./data/spanish_english.csv")
canvas_width = 800
canvas_height = 526
BACKGROUND_COLOR = "#B1DDC6"
PADDING = 40
FONT_NAME = "Arial"
english = ""
english_word = ""
front_language = ""
language_word = ""
count_timer = ""
language_index = 0
language_list = []
english_list = []
unique_ids = {"lang_id": 0, "word_id": 0, }


def switch_display(count):
    global count_timer
    if count > -1:
        right_button.config(command="")
        wrong_button.config(command="")
        count_timer = window.after(1000, switch_display, count - 1)
        front_card.grid()
        back_card.grid_remove()
    else:
        window.after_cancel(count_timer)
        back_card.grid()
        front_card.grid_remove()
        right_button.config(command=delete_items)
        wrong_button.config(command=reset)


def front_image(fronted_image):
    front_card.create_image(canvas_width/2, canvas_height/2, image=fronted_image)
    unique_ids["lang_id"] = front_card.create_text(canvas_width/2, canvas_height/3.5, fill="black",
                                                   text=front_language, font=(FONT_NAME, 26, "italic"))
    unique_ids["word_id"] = front_card.create_text(canvas_width/2, canvas_height/2, fill="black",
                                                   text=language_word, font=(FONT_NAME, 40, "bold"))


def back_image(backed_image):
    back_card.create_image(canvas_width/2, canvas_height/2, image=backed_image)
    unique_ids["lang_id"] = back_card.create_text(canvas_width/2, canvas_height/3.5, text=english,
                                                  font=(FONT_NAME, 26, "italic"))
    unique_ids["word_id"] = back_card.create_text(canvas_width/2, canvas_height/2, text=english_word,
                                                  font=(FONT_NAME, 40, "bold"))


def reset():
    manipulate_lists()
    front_card.delete(unique_ids["lang_id"], unique_ids["word_id"])
    back_card.delete(unique_ids["lang_id"], unique_ids["word_id"])
    frontier_image = PhotoImage(file="./images/card_front.png")
    backer_image = PhotoImage(file="./images/card_back.png")
    front_image(frontier_image)
    back_image(backer_image)
    switch_display(5)


def delete_items():
    reset()
    del language_list[language_index]
    del english_list[language_index]


def chosen_language(header, language_data):
    global front_language, english, language_list, english_list
    language_list = language_data[header].tolist()
    front_language = language_data[header].name
    english_list = language_data.English.tolist()
    english = language_data.English.name
    return language_list, english_list


def manipulate_lists():
    global language_word, english_word, language_index
    language_index = language_list.index(random.choice(language_list))
    language_word = language_list[language_index]
    english_word = english_list[language_index]
    return language_index


result = messagebox.askyesno(title="Choose Language", message="For French select 'Yes',"
                                                              " for Spanish, select 'No'.")
if result:
    chosen_language("French", french_data)
else:
    chosen_language("Spanish", spanish_data)

window = Tk()
window.title("Language Cards")
window.config(padx=PADDING, pady=PADDING, background=BACKGROUND_COLOR, highlightthickness=0)
manipulate_lists()

front_card = Canvas(width=canvas_width, height=canvas_height, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="./images/card_front.png")
front_image(front_img)
front_card.grid(row=0, column=0, columnspan=2)

back_card = Canvas(width=canvas_width, height=canvas_height, highlightthickness=0, bg=BACKGROUND_COLOR)
back_img = PhotoImage(file="./images/card_back.png")
back_image(back_img)
back_card.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, border=0)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, border=0)
wrong_button.grid(row=1, column=0)
switch_display(5)

window.mainloop()
