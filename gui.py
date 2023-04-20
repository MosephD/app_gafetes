import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, PhotoImage, ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import datetime
import subprocess
import shutil
import os

# THEME
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# --------------------------------------------
# Loading GAFETE images
# --------------------------------------------
user_homefolder = str(Path.home())
# Loading GAFETE Image File - FRONT
gafete_front = Image.open(
    user_homefolder + '/projects/app_gafetes/app_styled/assets/Frente.png')

gafete_front.save('preview.png')  # Reseting Preview

# Loading GAFETE Image File - BACK
gafete_back = Image.open(
    user_homefolder + '/projects/app_gafetes/app_styled/assets/Reverso.png')
gafete_back.save('preview-back.png')  # Reseting Preview

# Loading GAFETE Font File Location
fonts_folder = user_homefolder + '/projects/app_gafetes/app_styled/assets/Fonts/'


print(user_homefolder)
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
root = ctk.CTk()
root.geometry("569x718")  # WidthxHeight
root.maxsize(569, 718)
root.title("Gafetes")

previews_frame = ctk.CTkFrame(root, width=240, height=718, fg_color="#595959")
previews_frame.place(x=0, y=0,)


frame = ctk.CTkFrame(root, width=329, height=718, fg_color="#ffffff")
frame.place(x=240, y=0)


root.iconbitmap(r'assets/icon.ico')


# app_icon = PhotoImage(
#     file=user_homefolder + "/projects/app_gafetes/app_styled/assets/icon.png")
# root.iconphoto(False, app_icon)
# root.configure(bg='#FCF6E8')
# ----------------------------------------------------------------------------------------------------------------Displaying GAFETE preview

# front_preview_canvas = tk.Canvas(root, width=221, height=342)
# front_preview_canvas.create_rectangle(0, 0, 257, 354, fill="#1D1A12")
# front_preview_canvas.place(x=14, y=14)

# back_preview_canvas = tk.Canvas(root, width=221, height=342)
# back_preview_canvas.create_rectangle(0, 0, 257, 354, fill="#1D1A12")
# back_preview_canvas.place(x=14, y=369)

# -------------------------------

raw_preview = Image.open(
    'preview.png')
raw_preview_back = Image.open('preview-back.png')


width, height = 219, 340
resized_preview = raw_preview.resize((width, height))
resized_preview_back = raw_preview_back.resize((width, height))
# Convert the resized image to PhotoImage
converted_preview = ctk.CTkImage(resized_preview, size=(219, 340))
converted_preview_back = ctk.CTkImage(resized_preview_back, size=(219, 340))
# Create a CTkLabel widget to display the image
gafete_preview = ctk.CTkLabel(root, image=converted_preview, text=None, )
gafete_preview_back = ctk.CTkLabel(
    root, image=converted_preview_back, text=None)
# gafete_preview_back.config(image=converted_preview)
# gafete_preview_back_back.config(image=converted_preview_back)
gafete_preview.place(x=10, y=10)
gafete_preview_back.place(x=10, y=365)
# -------------------------------------------------------------------------
# Exit Button #--------------------


def close_app(event):
    root.destroy()


raw_exit_icon = Image.open(
    user_homefolder + '/projects/app_gafetes/app_styled/assets/logout.png')

exit_width, exit_height = 40, 40
resized_exit_icon = raw_exit_icon.resize((exit_width, exit_height))
converted_exit_icon = ctk.CTkImage(resized_exit_icon, size=(40, 40))

exit_icon = ctk.CTkLabel(root, image=converted_exit_icon,
                         text=None, fg_color="white")
exit_icon.place(x=516, y=649)
exit_icon.bind("<Button-1>", close_app)


# Save Button #--------------------
def save_result(event):
    first_name_text = first_name_field.get()
    last_name_text = last_name_field.get()
    export_gafete_folder = (user_homefolder +
                            '/Downloads/' + first_name_text + "_" + last_name_text)
    export_file_name = first_name_text + '_' + last_name_text + ".png"
    if os.path.exists(export_gafete_folder):
        shutil.rmtree(export_gafete_folder)
    os.makedirs(export_gafete_folder)
    export_front = (export_gafete_folder + '/' +
                    'Frente_' + export_file_name)
    export_back = (export_gafete_folder + '/' +
                   'Reverso_' + export_file_name)
    # print(export_front)
    gafete_front.save(export_front)
    gafete_back.save(export_back)
    formatted_path = os.path.normpath(export_gafete_folder)
    print(formatted_path)
    subprocess.Popen(r'explorer /open,"{}"'.format(formatted_path))


raw_save_icon = Image.open(
    user_homefolder + '/projects/app_gafetes/app_styled/assets/save.png')

save_width, save_height = 40, 40
resized_save_icon = raw_save_icon.resize((save_width, save_height))
converted_save_icon = ctk.CTkImage(resized_save_icon,  size=(36, 36))

save_icon = ctk.CTkLabel(root, image=converted_save_icon,
                         text=None, fg_color="white")
save_icon.place(x=455, y=650)
save_icon.bind("<Button-1>", save_result)

# --------------------------------------------------------------------------------------
#  Loading GAFETE 'Empleado Picture' File & Resizing/Cropping it -----------------------


def select_picture():
    global converted_preview
    filename = filedialog.askopenfilename()
    # Loading Picture File
    picture = Image.open(filename)
    # Loading Mask File
    mask = Image.open(
        user_homefolder + '/projects/app_gafetes/app_styled/assets/mask.png').convert('L')
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
    raw_preview = Image.open(
        'preview.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ctk.CTkImage(resized_preview, size=(219, 340))
    gafete_preview.configure(root, image=converted_preview, text=None)


# SELECTING PICTURE FROM COMPUTER BUTTON-------------------------------------------------
select_picture_CTkLabel = ctk.CTkLabel(
    root, text="Foto del Empleado:", font=("NotoSans", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# select_picture_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12")
select_picture_CTkLabel.place(x=256, y=20,)


# def user_picture():


select_picture_button = ctk.CTkButton(
    root, text="Buscar", command=select_picture, fg_color="#595959", corner_radius=7, font=("Catamaran", 15,), width=102)
# select_picture_button.config(
#     bg="#FCF6E8", fg="#1D1A12", font=("NotoSans-Bold", 9, "bold"))
select_picture_button.place(x=453, y=20,)

# --------------------------------------------------------------------------------------

# Validating user inputs


def validate_nss_input(value_if_allowed):

    if len(value_if_allowed) <= 13 and (value_if_allowed.isdigit() or value_if_allowed == "" or value_if_allowed[-1] == chr(8)):
        return True
    else:
        return False


def validate_numb_input(value_if_allowed):

    if len(value_if_allowed) <= 3 and (value_if_allowed.isdigit() or value_if_allowed == "" or value_if_allowed[-1] == chr(8)):
        return True
    else:
        return False


def validate_name_input(value_if_allowed):
    if len(value_if_allowed) <= 19 and all(c.isalpha() or c.isspace() for c in value_if_allowed):

        return True
    else:
        return False


def validate_position_input(value_if_allowed):
    if len(value_if_allowed) <= 22 and all(c.isalpha() or c.isspace() for c in value_if_allowed):

        return True
    else:
        return False

# ----------------------------------------------

# ---CLOSING---------


def hide_info_inputs():
    add_numb_button.place_forget()
    numb_field.place_forget()
    numb_CTkLabel.place_forget()
    add_bloodtype_button.place_forget()
    bloodtype_CTkLabel.place_forget()
    bloodtype_field.place_forget()
    add_nss_button.place_forget()
    nss_field.place_forget()
    nss_CTkLabel.place_forget()


# ---OPENING---------

def show_info_inputs():
    add_numb_button.place(x=530, y=405)
    numb_field.place(x=424, y=402)
    numb_CTkLabel.place(x=256, y=402)
    add_bloodtype_button.place(x=530, y=371)
    bloodtype_CTkLabel.place(x=256, y=362,)
    bloodtype_field.place(x=425, y=368)
    add_nss_button.place(x=530, y=325,)
    nss_field.place(x=350, y=322,)
    nss_CTkLabel.place(x=256, y=322,)


    # ----------------------------------------------
    # FIRTS NAME INPUT FIELD-------------------------------------------------
first_name_CTkLabel = ctk.CTkLabel(
    root, text="Nombre:", font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# first_name_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12")
first_name_CTkLabel.place(x=256, y=59,)


first_name_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
first_name_field.place(x=350, y=60,)
first_name_field.configure(validate="key",
                           validatecommand=(root.register(validate_name_input), '%P'))

# -------------------------------------------


# -------------------------------------------
# Storing First Name Input entry-------------------------------------------


def store_firstname_text(event):
    global changing_font
    global converted_preview
    name_font = changing_font(38)
    # store first name
    empleado_firstname = ''
    # get the text from the input field
    first_name_text = first_name_field.get()
    first_name_input = first_name_text
    print(type(first_name_input))
    print(first_name_input)
    empleado_firstname = first_name_input.title()
    w, h = textbox(empleado_firstname, 38)
    draw_name.rectangle((84, 539, 570, 577), fill='#727374')
    draw_name.text(((W-w)/2, ((H-h)/2)+47), empleado_firstname.title(),
                   font=name_font, fill='white')
    gafete_front.save('preview.png')
    raw_preview = Image.open(
        'preview.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ctk.CTkImage(resized_preview, size=(219, 340))
    gafete_preview.configure(root, image=converted_preview, text=None)


# Store field user input with a button
add_firstname_button = ctk.CTkButton(
    root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff")

add_firstname_button.place(x=530, y=62,)
# add_firstname_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
# Bind the field user input storing to keys and click
add_firstname_button.bind("<Button-1>",  store_firstname_text)
first_name_field.bind("<Button-1>", store_firstname_text)
first_name_field.bind("<Return>", store_firstname_text)
first_name_field.bind("<Tab>", store_firstname_text)

# -----------------------------------------------

# LAST NAME INPUT FIELD-----------------------------------------------
last_name_CTkLabel = ctk.CTkLabel(root, text="Apellido:",
                                  font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# last_name_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12", )
last_name_CTkLabel.place(x=256, y=101,)


last_name_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
last_name_field.place(x=350, y=100,)
last_name_field.configure(validate="key",
                          validatecommand=(root.register(validate_name_input), '%P'))

# Storing Last Name Input entry-------------------------------------------


def store_lastname_text(event):
    global changing_font
    global converted_preview
    name_font = changing_font(38)
    empleado_lastname = ''
    # get the text from the input field
    last_name_text = last_name_field.get()
    last_name_input = last_name_text
    print(last_name_input)
    empleado_lastname = last_name_input.title()
    # Draw 'First Name' text in image
    w, h = textbox(empleado_lastname, 38)
    draw_name.rectangle((94, 577, 555, 617), fill='#727374')
    draw_name.text(((W-w)/2, ((H-h)/2)+86), empleado_lastname.title(),
                   font=name_font, fill='white')
    gafete_front.save('preview.png')
    raw_preview = Image.open(
        'preview.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ctk.CTkImage(resized_preview, size=(219, 340))
    gafete_preview.configure(root, image=converted_preview, text=None)


# Store field user input with a button
add_lastname_button = ctk.CTkButton(root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff"
                                    )
add_lastname_button.place(x=530, y=103,)
# add_lastname_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
# Bind the field user input storing to keys and click
add_lastname_button.bind("<Button-1>",  store_lastname_text)
last_name_field.bind("<Button-1>", store_lastname_text)
last_name_field.bind("<Return>", store_lastname_text)
last_name_field.bind("<Tab>", store_lastname_text)


# ----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------

# POSITION INPUT FIELD-----------------------------------------------
position_CTkLabel = ctk.CTkLabel(root, text="Puesto:",
                                 font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# position_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12", )
position_CTkLabel.place(x=256, y=141,)


position_field = ctk.CTkEntry(
    root, fg_color="white", corner_radius=7,  width=170, font=("Amiko", 15))
position_field.place(x=350, y=140,)
position_field.configure(validate="key",
                         validatecommand=(root.register(validate_position_input), '%P'))

# -----------------------------------------------


# Storing Input entry-------------------------------------------


def store_position_text(event):
    global changing_font
    global converted_preview
    name_font = changing_font(28)
    empleado_position = ''
    # get the text from the input field
    position_text = position_field.get()
    position_input = position_text
    print(position_input)
    empleado_position = position_input.upper()
    # Draw 'Position' text in image
    w, h = textbox(empleado_position, 28)
    draw_name.rectangle((136, 615, 540, 657), fill='#727374')
    draw_name.text(((W-w)/2, ((H-h)/2)+123), empleado_position.upper(),
                   font=name_font, fill='white')
    gafete_front.save('preview.png')
    raw_preview = Image.open(
        'preview.png')
    resized_preview = raw_preview.resize((width, height))
    converted_preview = ctk.CTkImage(resized_preview, size=(219, 340))
    gafete_preview.configure(root, image=converted_preview, text=None)


# Store field user input with a button
add_position_button = ctk.CTkButton(root, text="+", width=24, height=24,   font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff"
                                    )
add_position_button.place(x=530, y=143,)
# add_position_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
# Bind the field user input storing to keys and click
add_position_button.bind("<Button-1>",  store_position_text)
position_field.bind("<Button-1>", store_position_text)
position_field.bind("<Return>", store_position_text)
position_field.bind("<Tab>", store_position_text)


# ----------------------------------------------------------------------------------------------------------------

side_separator = ttk.Separator(root, orient="horizontal")
side_separator.place(x=256, y=230, relwidth=1)


# ----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------

# DATE INPUT FIELD-----------------------------------------------
date_CTkLabel = ctk.CTkLabel(root, text="Fecha de Ingreso:",
                             font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# date_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12", )
date_CTkLabel.place(x=256, y=280,)


today = datetime.datetime.now()
date_cal = Calendar(root, selectmode='day',
                    year=today.year, month=today.month,
                    day=today.day)
# ----------------------------------------------
# Dictionary to map the numeric month values to string representations
month_map = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
}

# -------------------------------------------------------------------------------
# Storing Date Input-------------------------------------------


def display_date(event):
    hide_info_inputs()
    date_cal.place(x=256, y=318,)
    add_date_button.place(x=530, y=342)


def store_date(event):
    global changing_font
    global converted_preview_back
    global date_cal
    global month_map
    name_font = changing_font(38)
    # get the date from the calendar box
    date = date_cal.get_date()
    parsed_date = datetime.datetime.strptime(date, "%m/%d/%y")
    formatted_date = parsed_date.strftime(
        f"%e-{month_map[parsed_date.month]}-%y")
    print(formatted_date)
    # Draw 'Position' text in image
    draw_info.rectangle((366, 216, 615, 251), fill='white')
    draw_info.text((368, 215), formatted_date,
                   font=name_font, fill='#1D1E1B')
    # Print the size
    gafete_back.save('preview-back.png')
    raw_preview_back = Image.open(
        'preview-back.png')
    resized_preview_back = raw_preview_back.resize((width, height))
    converted_preview_back = ctk.CTkImage(
        resized_preview_back, size=(219, 340))
    gafete_preview_back.configure(
        root, image=converted_preview_back, text=None)

    date_cal.place_forget()
    add_date_button.place_forget()
    show_info_inputs()


#  Store date user input with a button
select_date_button = ctk.CTkButton(root, text="Seleccionar",  fg_color="#595959",  font=("Catamaran", 15), width=102
                                   )
select_date_button.place(x=453, y=282,)
add_date_button = ctk.CTkButton(root, text="+", width=24, height=24,  font=("NotoSans-Bold", 17, "bold",), text_color="#ffffff"
                                )


# add_date_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="lightgray", state='disable', font=("NotoSans-Bold", 9, "bold"))
# select_date_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
#  Bind the field user input storing to keys and click
select_date_button.bind("<Button-1>",  display_date)
add_date_button.bind("<Button-1>",  store_date)

# -------------------------------
# ----------------------------------------------------------------------------------------------------------------
# NSS INPUT FIELD-----------------------------------------------
nss_CTkLabel = ctk.CTkLabel(root, text="NSS:",
                            font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# nss_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12", )
nss_CTkLabel.place(x=256, y=322,)


nss_field = ctk.CTkEntry(root,  fg_color="white",
                         corner_radius=7,  width=170, font=("Amiko", 15))
nss_field.place(x=350, y=322,)
nss_field.configure(validate="key",
                    validatecommand=(root.register(validate_nss_input), '%P'))

# -----------------------------------------------
# Storing Input entry-------------------------------------------


def store_nss_text(event):
    global changing_font
    global converted_preview_back
    name_font = changing_font(38)
    empleado_nss = ''
    # get the text from the input field
    nss_text = nss_field.get()
    nss_input = nss_text
    print(nss_input)
    empleado_nss = nss_input.upper()
    # Draw 'nss' text in image
    draw_info.rectangle((255, 257, 640, 286), fill='white')
    draw_info.text((255, 257), empleado_nss.upper(),
                   font=name_font, fill='#1D1E1B')
    gafete_back.save('preview-back.png')
    raw_preview_back = Image.open(
        'preview-back.png')
    resized_preview_back = raw_preview_back.resize((width, height))
    converted_preview_back = ctk.CTkImage(
        resized_preview_back, size=(219, 340))
    gafete_preview_back.configure(
        root, image=converted_preview_back, text=None)


# Store field user input with a button
add_nss_button = ctk.CTkButton(root, text="+", width=24, height=24,  font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff"
                               )
add_nss_button.place(x=530, y=325,)
# add_nss_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
# Bind the field user input storing to keys and click
add_nss_button.bind("<Button-1>",  store_nss_text)
nss_field.bind("<Button-1>", store_nss_text)
nss_field.bind("<Return>", store_nss_text)

nss_field.bind("<Tab>", store_nss_text)


# ----------------------------------------------------------------------------------------------------------------

# -------------------------------
bloodtype_CTkLabel = ctk.CTkLabel(root, text="Tipo de sangre:",
                                  font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# bloodtype_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12", )
bloodtype_CTkLabel.place(x=256, y=362,)


# BLOODTYPE INPUT FIELD-----------------------------------------------

style = ttk.Style()
style.theme_use('clam')
# style.configure("TCombobox",
#                 background='#FCF6E8', fieldbackground='#FCF6E8', font=('NotoSans-Bold', 20, "bold"))
bloodtype_field = ctk.CTkComboBox(root,
                                  values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+'], fg_color="white", dropdown_fg_color="white", corner_radius=7, width=95, button_color="#595959", font=("Amiko", 14), dropdown_font=("Amiko", 14))
bloodtype_field.place(x=425, y=368)

# -----------------------------------------------


# Storing Input entry-------------------------------------------


def store_bloodtype_text(event):
    global changing_font
    global converted_preview_back
    name_font = changing_font(38)
    empleado_bloodtype = ''
    # get the text from the input field
    bloodtype_text = bloodtype_field.get()
    bloodtype_input = bloodtype_text
    print(bloodtype_input)
    empleado_bloodtype = bloodtype_input.upper()
    # Draw 'BloodType' text in image
    draw_info.rectangle((440, 299, 630, 330), fill='white')
    draw_info.text((440, 299), empleado_bloodtype.upper(),
                   font=name_font, fill='#1D1E1B')
    gafete_back.save('preview-back.png')
    raw_preview_back = Image.open(
        'preview-back.png')
    resized_preview_back = raw_preview_back.resize((width, height))
    converted_preview_back = ctk.CTkImage(
        resized_preview_back, size=(219, 340))
    gafete_preview_back.configure(
        root, image=converted_preview_back, text=None)


# Store field user input with a button
add_bloodtype_button = ctk.CTkButton(root, text="+", width=24, height=24,  font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff"
                                     )
add_bloodtype_button.place(x=530, y=371,)
# add_bloodtype_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
# Bind the field user input storing to keys and click
add_bloodtype_button.bind("<Button-1>",  store_bloodtype_text)
bloodtype_field.bind("<Button-1>", store_bloodtype_text)
bloodtype_field.bind("<Return>", store_bloodtype_text)
bloodtype_field.bind("<Tab>", store_bloodtype_text)


# ----------------------------------------------------------------------------------------------------------------


# -------------------------------
numb_CTkLabel = ctk.CTkLabel(root, text="Num. Empleado:",
                             font=("NotoSans-Bold", 20, "bold"),  fg_color="#ffffff", text_color="#595959")
# numb_CTkLabel.config(bg="#FCF6E8", fg="#1D1A12", )
numb_CTkLabel.place(x=256, y=402,)


# Numb INPUT FIELD-----------------------------------------------


numb_field = ctk.CTkEntry(root, fg_color="white", width=96, font=("Amiko", 15))
numb_field.place(x=424, y=402)
numb_field.configure(validate="key",
                     validatecommand=(root.register(validate_numb_input), '%P'))
# -----------------------------------------------


# Storing Input entry-------------------------------------------


def store_numb_text(event):
    global changing_font
    global converted_preview_back
    name_font = changing_font(38)
    empleado_numb = ''
    # get the text from the input field
    numb_text = numb_field.get()
    numb_input = numb_text
    print(numb_input)
    empleado_numb = numb_input.upper()
    # Draw 'numb' text in image
    draw_info.rectangle((427, 340, 620, 382), fill='white')
    draw_info.text((427, 340), empleado_numb.upper(),
                   font=name_font, fill='#1D1E1B')
    gafete_back.save('preview-back.png')
    raw_preview_back = Image.open(
        'preview-back.png')
    resized_preview_back = raw_preview_back.resize((width, height))
    converted_preview_back = ctk.CTkImage(
        resized_preview_back, size=(219, 340))
    gafete_preview_back.configure(
        root, image=converted_preview_back, text=None)


# Store field user input with a button
add_numb_button = ctk.CTkButton(root, text="+", width=24, height=24,  font=("NotoSans-Bold", 17, "bold"), text_color="#ffffff"
                                )
add_numb_button.place(x=530, y=405,)
# add_numb_button.config(
#     foreground='Black',  disabledforeground='#1D1A12', bg="#FCF6E8", state='disable', font=("NotoSans-Bold", 9, "bold"))
# Bind the field user input storing to keys and click
add_numb_button.bind("<Button-1>",  store_numb_text)
numb_field.bind("<Button-1>", store_numb_text)
numb_field.bind("<Return>", store_numb_text)
numb_field.bind("<Tab>", store_numb_text)


# ---------------------------------------------------------------------------------------------------------------
root.mainloop()
