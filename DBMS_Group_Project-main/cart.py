#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

import tkinter as tk 
from tkinter.ttk import *
from savedata import *
from PIL import Image, ImageTk
from db import *
from buynow import *
from ttkthemes import *

    

def cart():
    global img_list
    
    win = tk.Toplevel()
    win.geometry('1200x600')
    win.title('Cart')
    win.configure(bg = '#282c34')
    win.resizable(False, False)

    # ========== Styles ==========
    style = ThemedStyle()
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
        
    img_list = []
    items_list = []
    frames_list = []

    no_of_items = 0

    l = list(cart_info()[0])
    l.pop(0)

    for index, element in enumerate(l):
        if element != 0:
            no_of_items += 1
            items_list.append(index + 1)
    
    spin_names = ['spin_'+str(i) for i in range(no_of_items)]

    for i in range(no_of_items):    
        frame = tk.Frame(Products_Frame, height = 246, width = 900, bg = '#282c34', highlightbackground = 'white', highlightthickness = 1)
        frames_list.append(frame)
        frame.pack_propagate(0)
        frame.grid(row = i, column = 0, pady = 10)
        img = ImageTk.PhotoImage(Image.open("Products/Product " + str(items_list[i]) + "/1.jpg").resize((184,246)))
        img_list.append(img)
        img_label = Label(frame, image = img, style = 'Image.TLabel')
        
        data = get_info(items_list[i])
        
        name_label = Label(frame, text = data[2], style = 'cart_name.TLabel')
        price_label = Label(frame, text = '₹' + str(data[1]), style = 'cart_name.TLabel')
        delete_button = tk.Button(frame, text = 'Delete', bg = '#282c34', fg = '#219afc', bd = 0, padx = 100, command = lambda i = i: [frames_list[i].destroy(), update_cart(items_list[i], get_email(), 0)])
        
        
        def qty_func(i):
            update_cart(items_list[i], get_email(), spin_names[i].get())
        
        def update_label():
            total_price = 0
            price_list = get_price()
            l = list(cart_info()[0])
            l.pop(0)
            for j in range(len(price_list)):
                total_price += price_list[j]*l[j]
            total_price_label.configure(text = "Total Price : "+ '₹' + str(total_price))
        
        spin_names[i] = tk.IntVar()
        spin_names[i].set(l[i])
        qty = tk.Spinbox(frame, textvariable = spin_names[i], from_= 1, to = 10, width = 3, command = lambda i = i: [qty_func(i), update_label()])

        
        img_label.grid(row = 0, column = 0, padx = 20, pady = 10, rowspan = 2)
        name_label.grid(row = 0, column = 1, padx = 50)
        price_label.grid(row = 0, column = 2)
        qty.grid(row = 0, column = 3, padx = 50)
        delete_button.grid(row= 1, column = 1)
    
    
    total_price = 0
    price_list = get_price()
    for i in range(len(price_list)):
        total_price += price_list[i]*l[i]
    
    total_price_frame = tk.Frame(Products_Frame, height = 400, width = 200, bg = '#282c34', highlightthickness = 1, highlightcolor = 'white')
    total_price_label = Label(total_price_frame, text = "Total Price : "+ '₹' + str(total_price), style = 'cart_name.TLabel')
    proceed_to_buy_button = tk.Button(total_price_frame, text = 'Proceed to Buy', bg = '#fed25f', font = ('Times New Roman', 14, 'bold'), command = lambda: [buy_now(), win.destroy()])
    
    total_price_frame.grid(row = 0 , column = 1, padx = 50)
    total_price_label.pack(pady = 10, padx = 10)
    proceed_to_buy_button.pack(pady = 10)    

        
# root = tk.Tk()
# cart()
# root.mainloop()
    
    