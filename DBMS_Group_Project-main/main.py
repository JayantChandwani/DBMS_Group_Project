
# -*- coding: utf-8 -*-

from Account import *
from image_viewer import *
# from products import *
import tkinter as tk 
from tkinter.ttk import *
from ttkthemes import *
 
createdb()
createtable()
 
root = tk.Tk()
root.title("Shop")
root.configure(bg = '#282c34')
root.geometry("2000x1000")

# ========== Creating Styles ==========
style = ThemedStyle()
style.theme_use('ubuntu')
style.configure('Heading_main.TLabel', font = ("Times New Roman", 40, "bold"), foreground = 'white', background = '#282c34')
style.configure('image.TLabel', height = 246, width = 184, background = '#282c34')
 
# ========== Code to rewrite login_file on window closing ==========
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        update_file(False)
        update_email_file("")
        root.destroy()
 
root.protocol("WM_DELETE_WINDOW", on_closing)


# ======== Creating Widgets ========
Heading_frame = tk.Frame(root)
Heading_frame.grid(row = 0, column = 0)
 
Heading = Label(Heading_frame, text = 'SHOP', style = 'Heading_main.TLabel')
Heading.pack()
 
Account_frame = tk.Frame(root, bg = '#282c34')
Account_frame.place(x = 1350, y = 0)
 
signin_button = tk.Button(Account_frame, text='Sign in', padx = 10, pady = 10, command = signin, bg = '#3276fc', fg = 'white', font = 'Impact')
login_button = tk.Button(Account_frame, text='Log in', padx = 10, pady = 10, command = lambda: user_login(Account_frame), bg = '#3276fc', fg = 'white', font = 'Impact')

signin_button.grid(row = 0, column = 1, padx = 1)
login_button.grid(row = 0, column = 2, padx = 1)

# Creating a Frame for the canvas
canvas_frame = tk.Frame(root, height = 700, width = 1500)
canvas_frame.pack_propagate(0)
canvas_frame.grid(row = 1, column = 0, columnspan = 2)

# Creating and placing a canvas in the canvas Frame
my_canvas = tk.Canvas(canvas_frame, bg = '#282c34', bd=0, highlightthickness=0)
my_canvas.pack(side = 'left', fill = 'both', expand = 'yes')

# Creating a Scrollbar
yscroll = Scrollbar(canvas_frame, orient = 'vertical', command = my_canvas.yview)
yscroll.pack(side = 'right', fill = 'y')

# Configuring the Canvas
my_canvas.configure(yscrollcommand = yscroll.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

# Creating the product frame which goes in the canvas
Products_Frame = tk.Frame(my_canvas, width = 2000, height = 1000, bg = '#282c34')

# Adding a window to the canvas
my_canvas.create_window((0,0), window = Products_Frame, anchor = 'nw')

# login function used for login button widget
def user_login(Account_frame):
    login_state = read_file()[0]
    login(login_state, Account_frame)
 
 
c = 0
frame_list = []

# Required because images created in functions and loops get garbage collected and hence need to be made global
img_list = []
no_list = [4, 4, 2, 3, 5, 4 ,4, 4]


# ========== Creating and Placing Widgets ==========
for i in range(0, 8):
    data = get_info(i+1)
    
    if i % 3 == 0 and i != 0:
        c += 1

    frame = tk.Frame(Products_Frame, bg = '#282c34', padx = 10, pady = 10, height = 320, width = 400)
    
    # This Method Fixes the height and width of the frame
    frame.pack_propagate(0)
    
    frame_list.append(frame)
    frame.grid(row = c, column = i%3, padx = 50, pady = 50)
    img = ImageTk.PhotoImage(Image.open("Products/Product " + str(i+1) + "/1.jpg").resize((184,246)))
    img_list.append(img)
    img_lable = Label(frame, image = img, style = 'image.TLabel')
    price_label = tk.Label(frame, text = '₹' + str(data[1]), font = ('Times New Roman', 15, 'bold'), fg = 'white', bg = '#282c34')
    name_label = tk.Button(frame, text = data[2], command = lambda i = i: viewitem((i+1), no_list[i]), font = ('Times New Roman', 12), fg = 'white', bg = '#282c34', bd = 0, relief = 'flat')
    
    img_lable.pack()
    name_label.pack()
    price_label.pack()
    

root.mainloop()
