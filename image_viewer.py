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
import os


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
    # Create as tk.Frame with bg already set in constructor
    my_frame = tk.Frame(win, width ='723', height = '382', bg='#282c34')
    my_frame.pack_propagate(0)
    frame.place(x=0, y=0)
    my_frame.place(x=410, y=0)

    image_list = []

    # Try to load images, handle missing images gracefully
    for i in range(1, img_number + 1):
        try:
            img_path = f"Products/Product {product_number}/{i}.jpg"
            if os.path.exists(img_path):
                image_list.append(ImageTk.PhotoImage(Image.open(img_path).resize((400, 550))))
            else:
                print(f"Image not found: {img_path}")
        except Exception as e:
            print(f"Error loading image {i} for product {product_number}: {str(e)}")

    # If no images were successfully loaded, add a placeholder
    if not image_list:
        try:
            image_list.append(ImageTk.PhotoImage(Image.open("Products/placeholder.jpg").resize((400, 550))))
        except Exception as e:
            print(f"Error loading placeholder image: {str(e)}")
            # Create a blank image if placeholder can't be loaded
            img = Image.new('RGB', (400, 550), color='#cccccc')
            image_list.append(ImageTk.PhotoImage(img))

    actual_img_count = len(image_list)
    status = Label(frame, text="Image 1 of " + str(actual_img_count), style = 'status.TLabel')

    # Creating a Label to hold the image 
    my_label = Label(frame, image=image_list[0])
    my_label.grid(row = 0, column = 0, columnspan = 3)

    # Function to switch to the next image    
    def forward(image_number):
        if image_number <= actual_img_count:        
            my_label.config(image=image_list[image_number - 1])
            
            back_button['command'] = lambda: back(image_number - 1)
            forward_button['command'] = lambda: forward(image_number + 1)

            if image_number == actual_img_count:
                back_button.config(state='!disabled')
                forward_button.config(state='disabled')
            else:
                back_button.config(state='!disabled')
                forward_button.config(state='!disabled')

            status.config(text="Image " + str(image_number) + " of " + str(actual_img_count))

    # Function to switch to the previous image
    def back(image_number):
        if image_number >= 1:
            my_label.config(image=image_list[image_number - 1])

            back_button['command'] = lambda: back(image_number - 1)
            forward_button['command'] = lambda: forward(image_number + 1)

            if image_number == 1:
                back_button.config(state='disabled')
                forward_button.config(state='!disabled')
            else:
                back_button.config(state='!disabled')
                forward_button.config(state='!disabled')

            status.config(text="Image " + str(image_number) + " of " + str(actual_img_count))

    # Creating  and placing widgets
    back_button = Button(frame, text = '<',command = back, state = 'disabled')
    back_button.grid(row = 1, column = 0)

    forward_button = Button(frame, text = '>', command = lambda: forward(2))
    forward_button.grid(row = 1, column = 2)

    status.grid(row = 2, column=0, columnspan = 3, sticky = 'we')
    
    # Creating Widgets for my_frame (avoid redundant bg configuration)
    sep1 = Separator(my_frame, orient = 'horizontal')
    sep2 = Separator(my_frame, orient = 'horizontal')
    data = get_info(product_number)
    
    # Create fonts for consistency
    name_font = ('Times New Roman', 24, 'bold')
    desc_font = ('Times New Roman', 12)
    price_font = ('Times New Roman', 20, 'bold')
    
    # Use tk widgets without ttk styling
    name = tk.Label(my_frame, text=data[2], font=name_font, bg='#282c34', fg='white', wraplength=700, justify='center')
    
    add_to_cart_frame = Frame(win)
    add_to_cart_frame.place(relx = 0.36, rely = 0.6)
    add_to_cart_btn = tk.Button(add_to_cart_frame, text = 'Add To Cart', bg = '#fed25f', font = ('Times New Roman', 14, 'bold'), command = lambda : add_to_cart_func(product_number, win)).pack(pady = 3)

    desc_list = data[3].split(';')
    desc = str('\n'.join(desc_list))
    
    # Use tk.Message without style for description
    description = tk.Message(my_frame, text=desc, width=700, anchor='w', bg='#282c34', fg='white', font=desc_font)
    
    # Use tk.Label for price with consistent styling
    price = tk.Label(my_frame, text='₹' + str(data[1]), font=price_font, bg='#282c34', fg='#fed25f')

    # Placing Widgets on my_frame with padding
    name.grid(row=0, column=0, pady=(10, 20))
    sep1.grid(row=1, column=0, sticky='we', pady=5)
    price.grid(row=2, column=0, pady=10)
    sep2.grid(row=3, column=0, sticky='we', pady=5)
    description.grid(row=4, column=0, sticky='we', pady=10)


# root = tk.Tk()
# viewitem(3, 2)
# root.mainloop()