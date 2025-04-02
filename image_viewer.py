#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import tkinter as tk 
from tkinter.ttk import *
from PIL import ImageTk,Image
from db import *
from savedata import *
from cart import *
import tkinter.messagebox as messagebox
from ttkthemes import *
from db import c  # Import the cursor


def add_to_cart_func(product_number, win):
    from db import c as db_cursor  # Import cursor locally
    
    email = get_email()
    if email != "":
        # Check if product exists
        db_cursor.execute("USE SHOPPING;")
        db_cursor.execute("SELECT COUNT(*) FROM product WHERE pid = %s;", (product_number,))
        if db_cursor.fetchone()[0] == 0:
            messagebox.showerror("", "Product does not exist")
            return
            
        # Get current quantity in cart
        db_cursor.execute("SELECT quantity FROM cart_items WHERE email = %s AND product_id = %s;", 
                 (email, product_number))
        result = db_cursor.fetchone()
        
        current_qty = result[0] if result else 0
            
        if current_qty < 10:  # Max 10 items per product
            update_cart(product_number, email, current_qty + 1)
            messagebox.showinfo("","Product Added to Cart")
        else:
            messagebox.showinfo("","Maximum quantity (10) reached for this item")
            
        win.destroy()
    else:
        messagebox.showinfo("","Please Login Before Adding To Cart")

def viewitem(product_number, img_number):
    global my_label
    win = tk.Toplevel()
    win.geometry('1200x600')
    win.title("Product")
    
    style = ThemedStyle()
    style.theme_use('ubuntu')
    style.configure("status.TLabel", foreground="black", background="white", relief = 'sunken', anchor = 'e', bd = 1)
    style.configure('a.TLabel', font = ('Times New Roman', 24, 'bold'), width = '400', justify = 'center')

    frame = Frame(win, width = '400', height = '600')
    my_frame = Frame(win, width ='723', height = '382')
    my_frame.pack_propagate(0)
    frame.place(x=0, y=0)
    my_frame.place(x=410, y=0)

    image_list = []

    for i in range(1, img_number + 1):
        image_list.append(ImageTk.PhotoImage(Image.open("Products/Product " + str(product_number) + "/"+ str(i) +".jpg").resize((400, 550))))

    status = Label(frame, text="Image 1 of " + str(len(image_list)), style = 'status.TLabel')

    # Creating a Label to hold the image 
    my_label = Label(frame, image=image_list[0])
    my_label.grid(row = 0, column = 0, columnspan = 3)

    # Function to switch to the next image    
    def forward(image_number):        
        my_label.config(image=image_list[image_number - 1])
        
        back_button['command'] = lambda: back(image_number - 1)
        forward_button['command'] = lambda: forward(image_number +1)

        if image_number == img_number:
            back_button.config(state='!disabled')
            forward_button.config(state='disabled')
        else:
            back_button.config(state='!disabled')
            forward_button.config(state='!disabled')

        status.config(text="Image " + str(image_number) + " of " + str(len(image_list)))

    # Function to switch to the previous image
    def back(image_number):
        my_label.config(image=image_list[image_number - 1])

        back_button['command'] = lambda: back(image_number - 1)
        forward_button['command'] = lambda: forward(image_number +1)

        if image_number == 1:
            back_button.config(state='disabled')
            forward_button.config(state='!disabled')
        else:
            back_button.config(state='!disabled')
            forward_button.config(state='!disabled')

        status.config(text="Image " + str(image_number) + " of " + str(len(image_list)))
        
    # Creating  and placing widgets
    back_button = Button(frame, text = '<',command = back, state = 'disabled')
    back_button.grid(row = 1, column = 0)

    forward_button = Button(frame, text = '>', command = lambda: forward(2))
    forward_button.grid(row = 1, column = 2)

    status.grid(row = 2, column=0, columnspan = 3, sticky = 'we')
    
    # Creating Widgets for my_frame
    
    sep1 = Separator(my_frame, orient = 'horizontal')
    sep2 = Separator(my_frame, orient = 'horizontal')
    data = get_info(product_number)
    name = Label(my_frame, text = data[2], style = 'a.TLabel')
    
    add_to_cart_frame = Frame(win)
    add_to_cart_frame.place(relx = 0.36, rely = 0.6)
    add_to_cart_btn = tk.Button(add_to_cart_frame, text = 'Add To Cart', bg = '#fed25f', font = ('Times New Roman', 14, 'bold'), command = lambda : add_to_cart_func(product_number, win)).pack(pady = 3)

    
    desc_list = data[3].split(';')
    desc = str('\n'.join(desc_list))
    
            
    description = tk.Message(my_frame, text = desc, width = '723', anchor = 'w')
    price = Label(my_frame, text = '₹' + str(data[1]), style = 'a.TLabel')

    # Placing Widgets on my_frame
    name.grid(row=0, column =0)
    sep1.grid(row = 1, column = 0, sticky = 'we')
    price.grid(row=2, column =0)
    sep2.grid(row = 3, column = 0, sticky = 'we')
    description.grid(row=4, column = 0, sticky = 'we')


# root = tk.Tk()
# viewitem(3, 2)
# root.mainloop()