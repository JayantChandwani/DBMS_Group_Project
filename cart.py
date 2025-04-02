#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import tkinter as tk 
from tkinter.ttk import *
from savedata import *
from PIL import Image, ImageTk
from db import *
from buynow import *
from db import c  # Import the cursor
    

def calculate_total_price():
    from db import c as db_cursor  # Import cursor locally
    
    # Get cart items for the current user
    email = get_email()
    
    db_cursor.execute("USE SHOPPING;")
    db_cursor.execute("""
        SELECT ci.product_id, ci.quantity, p.price
        FROM cart_items ci
        JOIN product p ON ci.product_id = p.pid
        WHERE ci.email = %s
    """, (email,))
    
    cart_items = db_cursor.fetchall()
    
    # Calculate total price
    total = sum(item[1] * item[2] for item in cart_items)
    return total


def cart():
    global img_list
    
    win = tk.Toplevel()
    win.geometry('1200x600')
    win.title('Cart')
    win.configure(bg = '#282c34')
    win.resizable(False, False)

    # ========== Styles ==========
    style = Style()
    style.configure('cart_heading.TLabel', font = 'Impact 32', background = '#282c34', foreground = 'white')
    style.configure('cart_name.TLabel', font = ('Times New Roman', 14 ,'bold'), background = '#282c34', foreground = 'white')

    # ========== Heading ==========
    Heading = Label(win, text = 'Shopping Cart', style = 'cart_heading.TLabel')
    Heading.grid(row = 0, column = 0, sticky = 'we')
    
    
    # Creating a Frame for the canvas
    canvas_frame = tk.Frame(win, height = 495, width = 1200)
    canvas_frame.pack_propagate(0)
    canvas_frame.grid(row = 1, column = 0, columnspan = 2, pady = 50)

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
    
    # Create total price frame and label first
    total_price_frame = tk.Frame(Products_Frame, height = 400, width = 200, bg = '#282c34', highlightthickness = 1, highlightcolor = 'white')
    total_price_label = Label(total_price_frame, text = "", style = 'cart_name.TLabel')
    proceed_to_buy_button = tk.Button(total_price_frame, text = 'Proceed to Buy', bg = '#fed25f', font = ('Times New Roman', 14, 'bold'), command = lambda: [buy_now(), win.destroy()])
    
    total_price_frame.grid(row = 0, column = 1, padx = 50)
    total_price_label.pack(pady = 10, padx = 10)
    proceed_to_buy_button.pack(pady = 10)
        
    img_list = []
    items_list = []
    frames_list = []
    
    # Function to update total price label
    def update_total_price():
        total = calculate_total_price()
        total_price_label.configure(text = "Total Price : "+ '₹' + str(total))
        return total

    # Function to handle product deletion
    def delete_product(item_id, frame):
        # First update database
        update_cart(item_id, get_email(), 0)
        # Then remove visual frame
        frame.destroy()
        # Finally update the total price
        win.after(100, update_total_price)  # Small delay to ensure DB update completes

    # Get cart items for the current user
    email = get_email()
    
    from db import c as db_cursor  # Import cursor locally
    db_cursor.execute("USE SHOPPING;")
    db_cursor.execute("""
        SELECT ci.product_id, ci.quantity, p.name, p.price
        FROM cart_items ci
        JOIN product p ON ci.product_id = p.pid
        WHERE ci.email = %s
        ORDER BY ci.product_id
    """, (email,))
    
    cart_items = db_cursor.fetchall()
    no_of_items = len(cart_items)
    
    # Create a list of product IDs in the cart
    for item in cart_items:
        items_list.append(item[0])  # product_id
    
    spin_names = ['spin_'+str(i) for i in range(no_of_items)]

    # Function to handle quantity updates with validation and real-time price changes
    def update_qty(i):
        def callback(*args):  # Wrapper function to handle trace args
            try:
                new_qty = int(spin_names[i].get())
                # Prevent any value below 1
                if new_qty < 1:
                    spin_names[i].set(1)
                    update_cart(items_list[i], get_email(), 1)
                elif new_qty > 10:
                    spin_names[i].set(10)
                    update_cart(items_list[i], get_email(), 10)
                else:
                    update_cart(items_list[i], get_email(), new_qty)
                update_total_price()
            except ValueError:
                spin_names[i].set(1)
                update_cart(items_list[i], get_email(), 1)
                update_total_price()
        return callback

    for i in range(no_of_items):
        product_id = items_list[i]
        quantity = cart_items[i][1]
        name = cart_items[i][2]
        price = cart_items[i][3]
        
        frame = tk.Frame(Products_Frame, height = 246, width = 900, bg = '#282c34', highlightbackground = 'white', highlightthickness = 1)
        frames_list.append(frame)
        frame.pack_propagate(0)
        frame.grid(row = i, column = 0, pady = 10)
        
        # Try to load product image, use placeholder if not found
        try:
            img = ImageTk.PhotoImage(Image.open(f"Products/Product {product_id}/1.jpg").resize((184,246)))
        except:
            img = ImageTk.PhotoImage(Image.open("Products/placeholder.jpg").resize((184,246)))
            
        img_list.append(img)
        img_label = Label(frame, image = img, style = 'Image.TLabel')
        
        name_label = Label(frame, text = name, style = 'cart_name.TLabel')
        price_label = Label(frame, text = '₹' + str(price), style = 'cart_name.TLabel')
        
        delete_button = tk.Button(frame, text = 'Delete', bg = '#282c34', fg = '#219afc', bd = 0, padx = 100,
                                command = lambda id=product_id, f=frame: delete_product(id, f))
        
        # Initialize spinbox with minimum value 1
        spin_names[i] = tk.IntVar()
        spin_names[i].set(max(1, quantity))  # Use the actual quantity from database
        
        # Create spinbox with strict validation for values 1-10
        qty = tk.Spinbox(frame, 
                        textvariable=spin_names[i],
                        from_=1, to=10, width=3,
                        validate='all',
                        validatecommand=(frame.register(
                            lambda x: x.isdigit() and (x == "" or 1 <= int(x) <= 10)), '%P'))
        
        # Bind variable trace using closure
        spin_names[i].trace_add("write", update_qty(i))

        # Update grid layout
        img_label.grid(row = 0, column = 0, padx = 20, pady = 10, rowspan = 2)
        name_label.grid(row = 0, column = 1, padx = 50)
        price_label.grid(row = 0, column = 2)
        qty.grid(row = 0, column = 3, padx = 50)
        delete_button.grid(row = 1, column = 1)
    
    # Calculate initial total price
    update_total_price()




