import tkinter as tk
from tkinter import filedialog, PhotoImage
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import os


# Loading GAFETE Image File - FRONT
gafete_front = Image.open(
    'C:\\Users\\medin\\Projects\\pillower\\assets\\images\\plain-gafete-front.png')
gafete_front.save('preview.png')

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
root.geometry("900x600")
# ----------------------------------------------------------------------------------------------------------------Displaying GAFETE preview


raw_preview = Image.open(
    'C:\\Users\\medin\\Projects\\app_gafetes\\app\\preview.png')


width, height = 262, 408
resized_preview = raw_preview.resize((width, height))
# Convert the resized image to PhotoImage
converted_preview = ImageTk.PhotoImage(resized_preview)
print(converted_preview)
# Create a Label widget to display the image
gafete_preview = tk.Label(root)
gafete_preview.config(image=converted_preview)
gafete_preview.place(x=0, y=0,)


# ----------------------------------------------------------------------------------------------------------------
# FIRTS NAME INPUT FIELD-------------------------------------------------
first_name_label = tk.Label(root, text="Nombre:", font=("Oxygen", 14, "bold"))
first_name_label.place(x=282, y=0,)


first_name_field = tk.Entry(root)
first_name_field.place(x=330, y=0,)
first_name_field.config(width=20, font=("Oxygen", 12, "bold"))

# -------------------------------------------

name_font = changing_font(38)

# -------------------------------------------
# Storing Input entry-------------------------------------------


def store_firstname_text(event):
    global converted_preview
    # store first name
    empleado_firstname = ''
    # get the text from the input field
    first_name_text = first_name_field.get()
    first_name_input = first_name_text
    print(first_name_input)
    empleado_firstname = first_name_input
    # Draw 'First Name' text in image
    w, h = textbox(empleado_firstname, 38)
    draw_name.text(((W-w)/2, ((H-h)/2)+48), empleado_firstname.title(),
                   font=name_font, fill='white')
    gafete_front.save('preview.png')
    raw_preview = Image.open(
        'C:\\Users\\medin\\Projects\\app_gafetes\\app\\preview.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ImageTk.PhotoImage(resized_preview)
    print(converted_preview)
    gafete_preview.config(image=converted_preview)


# Store field user input with a button
add_firstname_button = tk.Button(
    root, text="Agregar",)

add_firstname_button.place(x=460, y=0,)
add_firstname_button.config(
    foreground='Black',  disabledforeground='Black', background='light gray', state='disable')
# Bind the field user input storing to keys and click
add_firstname_button.bind("<Button-1>",  store_firstname_text)
# first_name_field.bind("<Button-1>", store_firstname_text)
first_name_field.bind("<Return>", store_firstname_text)
first_name_field.bind("<Tab>", store_firstname_text)

# ----------------------------------------------------------------------------------------------------------------
# LAST NAME INPUT FIELD-----------------------------------------------
last_name_label = tk.Label(root, text="Apellido:", font=("Oxygen", 14, "bold"))
last_name_label.grid(row=2, column=3, padx=5, pady=5)


last_name_field = tk.Entry(root)
last_name_field.grid(row=2, column=4, padx=10, pady=10)
last_name_field.config(width=20, font=("Oxygen", 12, "bold"))

# Storing Input entry-------------------------------------------


def store_lastname_text(event):
    empleado_lastname = ''
    # get the text from the input field
    last_name_text = last_name_field.get()
    last_name_input = last_name_text
    print(last_name_input)
    empleado_lastname = last_name_input
    # Draw 'First Name' text in image
    w, h = textbox(empleado_lastname, 38)
    draw_name.text(((W-w)/2, ((H-h)/2)+83), empleado_lastname.title(),
                   font=name_font, fill='white')
    gafete_front.save('preview.png')


# Store field user input with a button
add_lastname_button = tk.Button(root, text="Agregar",
                                )
add_lastname_button.grid(row=2, column=5)
add_lastname_button.config(
    foreground='Black',  disabledforeground='Black', background='light gray', state='disable')
# Bind the field user input storing to keys and click
add_lastname_button.bind("<Button-1>",  store_lastname_text)
last_name_field.bind("<Button-1>", store_lastname_text)
last_name_field.bind("<Return>", store_lastname_text)
last_name_field.bind("<Tab>", store_lastname_text)


# ----------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
#  Loading GAFETE 'Empleado Picture' File & Resizing/Cropping it -----------------------


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
    print(filename)
    gafete_front.save('preview.png')

    gafete_front.save('Result.png')


# SELECTING PICTURE FROM COMPUTER BUTTON-------------------------------------------------
select_picture_button = tk.Button(
    root, text="Select Picture", command=select_picture)
select_picture_button.grid(row=3, column=3, padx=10, pady=10)
# --------------------------------------------------------------------------------------


root.mainloop()
