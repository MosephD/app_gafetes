import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


# Loading GAFETE Image File - FRONT
gafete_front = Image.open(
    'C:\\Users\\medin\\Projects\\pillower\\assets\\images\\plain-gafete-front.png')

# Loading GAFETE Image File - BACK
gafete_back = Image.open(
    'C:\\Users\\medin\\Projects\\pillower\\assets\\images\\plain-gafete-back.png')

# Loading GAFETE Font File Location
fonts_folder = 'C:\\Users\\medin\\AppData\\Local\\Microsoft\Windows\\Fonts'


#  Selecting GAFETE Font File & Font Size------------------------------------


def changing_font(font_size):
    name_font = ImageFont.truetype(os.path.join(
        fonts_folder, "Nexa Bold.otf"), font_size)
    return name_font


# Select the front side image of GAFETE
draw_name = ImageDraw.Draw(gafete_front)

# Select the back side image of GAFETE
draw_info = ImageDraw.Draw(gafete_back)

# Get front side image Width and Height values
W, H = gafete_front.size
# -------------------------------------------------------------


def textbox(current_draw, size):  # Creating textboxes
    _, _, w, h = draw_name.textbbox(
        (0, 0), current_draw, font=changing_font(size))  # aqui esta el pedo
    return w, h


# -------------------------------------------------------------

# Creating APP Window-----------------------------------------------
root = tk.Tk()
root.geometry("800x600")


#  Loading GAFETE 'Empleado Picture' File & Resizing/Cropping it -------------------------------------------------------------------------

# Loading Picture File
# picture = Image.open(
#     select_picture)


# --------------------------------------------------------------------------------------
# SELECTING PICTURE FROM COMPUTER BUTTON-------------------------------------------------


def select_picture():
    filename = filedialog.askopenfilename()
    # Loading Picture File
    picture = Image.open(filename)
    # Loading Mask File
    mask = Image.open(
        'C:\\Users\\medin\\Projects\\pillower\\assets\\mask.png').convert('L')
    # Creating Mask
    picture_output = ImageOps.fit(picture, mask.size, centering=(0.5, 0.5))
    picture_output.putalpha(mask)
    # Draw 'Picture' image in image
    w, h = picture_output.size
    cords = ((W-w)/2, (H-h)/2-206)
    cords = tuple(round(x) for x in cords)
    gafete_front.paste(picture_output, cords, picture_output)


gafete_front.save('Frente.png')
select_picture_button = tk.Button(
    root, text="Select Picture", command=select_picture)
select_picture_button.grid(row=0, column=2, padx=10, pady=10)

# FIRTS NAME INPUT FIELD-------------------------------------------------

first_name_field = tk.Entry(root)
first_name_field.grid(row=1, column=2, padx=10, pady=10)

# Storing Input entry-------------------------------------------


def store_text(event):
    # get the text from the input field
    name_text = first_name_field.get()
    name_input = name_text
    print(name_input)


first_name_field.bind("<Return>", store_text)
first_name_field.bind("<Tab>", store_text)

# LAST NAME INPUT FIELD-----------------------------------------------
last_name_field = tk.Entry(root)
last_name_field.grid(row=2, column=2, padx=10, pady=10)


# -------------------------------------------------------------


root.mainloop()
