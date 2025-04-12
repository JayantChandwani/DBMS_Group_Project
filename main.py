# -*- coding: utf-8 -*-

from Account import *
from image_viewer import *
from RetailerAccount import *  # Import retailer functionality
import tkinter as tk 
from tkinter.ttk import *
from ttkthemes import *
from db import c  # Import the cursor

createdb()
createtable()

root = tk.Tk()
root.title("Shop")
root.configure(bg = '#282c34')
root.geometry("1600x900")  # More standard size

# ========== Creating Styles ==========
style = ThemedStyle()
style.theme_use('ubuntu')
style.configure('Heading_main.TLabel', font = ("Times New Roman", 40, "bold"), foreground = 'white', background = '#282c34')
style.configure('image.TLabel', height = 246, width = 184, background = '#282c34')
style.configure('section_label.TLabel', font = ("Times New Roman", 16, "bold"), foreground = 'white', background = '#282c34')
style.configure('divider.TFrame', background = '#3a3f4b', height = 2)

# ========== Code to rewrite login_file on window closing ==========
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        update_file(False)
        update_email_file("")
        update_retailer_file(False)
        update_retailer_email_file("")
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# ======== Creating Main Layout Structure ========
# Top header frame
header_frame = tk.Frame(root, bg='#282c34', height=80)
header_frame.pack(fill='x', pady=(0, 5))
header_frame.pack_propagate(0)  # Prevent shrinking

# Header content
Heading = Label(header_frame, text='ONLINE SHOP', style='Heading_main.TLabel')
Heading.pack(side='left', padx=20)

# Divider after header
divider1 = tk.Frame(root, height=2, bg='#3a3f4b')
divider1.pack(fill='x')

# Account section frame
accounts_section_frame = tk.Frame(root, bg='#282c34', height=60)
accounts_section_frame.pack(fill='x')
accounts_section_frame.pack_propagate(0)  # Prevent shrinking

# Account section labels
customer_label = Label(accounts_section_frame, text='CUSTOMER', style='section_label.TLabel')
customer_label.pack(side='left', padx=(20, 0))

retailer_label = Label(accounts_section_frame, text='RETAILER', style='section_label.TLabel')
retailer_label.pack(side='left', padx=(300, 0))

# Account buttons frames
Account_frame = tk.Frame(accounts_section_frame, bg='#282c34')
Account_frame.pack(side='left', padx=(50, 0))

Retailer_frame = tk.Frame(accounts_section_frame, bg='#282c34')
Retailer_frame.pack(side='left', padx=(50, 0))

# Refresh button on the right
refresh_button = tk.Button(accounts_section_frame, text="Refresh Products", command=lambda: refresh_products(), 
                         bg='#3276fc', fg='white', font=('Times New Roman', 12),
                         padx=10, pady=5)
refresh_button.pack(side='right', padx=20)

# Divider after account section
divider2 = tk.Frame(root, height=2, bg='#3a3f4b')
divider2.pack(fill='x', pady=(5, 10))

# Main content frame for products
content_frame = tk.Frame(root, bg='#282c34')
content_frame.pack(fill='both', expand=True, padx=20, pady=10)

# Creating a Frame for the canvas
canvas_frame = tk.Frame(content_frame, bg='#282c34')
canvas_frame.pack(fill='both', expand=True)

# Creating and placing a canvas in the canvas Frame
my_canvas = tk.Canvas(canvas_frame, bg='#282c34', bd=0, highlightthickness=0)
my_canvas.pack(side='left', fill='both', expand=True)

# Creating a Scrollbar
yscroll = Scrollbar(canvas_frame, orient='vertical', command=my_canvas.yview)
yscroll.pack(side='right', fill='y')

# Configuring the Canvas
my_canvas.configure(yscrollcommand=yscroll.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Creating the product frame which goes in the canvas
Products_Frame = tk.Frame(my_canvas, bg='#282c34')
Products_Frame.columnconfigure(0, weight=1)
Products_Frame.columnconfigure(1, weight=1)
Products_Frame.columnconfigure(2, weight=1)

# Adding a window to the canvas
my_canvas.create_window((0,0), window=Products_Frame, anchor='nw')

# Initialize account buttons
signin_button = tk.Button(Account_frame, text='Sign in', padx=10, pady=5, command=signin, 
                        bg='#3276fc', fg='white', font=('Times New Roman', 12, 'bold'))
login_button = tk.Button(Account_frame, text='Log in', padx=10, pady=5, command=lambda: user_login(Account_frame, Retailer_frame), 
                       bg='#3276fc', fg='white', font=('Times New Roman', 12, 'bold'))

signin_button.grid(row=0, column=0, padx=5)
login_button.grid(row=0, column=1, padx=5)

# Initialize the retailer frame with sign up and login buttons
init_retailer_frame(Retailer_frame, Account_frame)

# login function used for login button widget
def user_login(Account_frame, Retailer_frame):
    login_state = read_file()[0]
    login(login_state, Account_frame, Retailer_frame)

row_counter = 0  # Renamed from c
frame_list = []

# Required because images created in functions and loops get garbage collected and hence need to be made global
img_list = []
no_list = []  # This will now be dynamically populated

# Simplify add_to_cart to always add 1 item
def add_to_cart(product_number):
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
    else:
        messagebox.showinfo("","Please Login Before Adding To Cart")

# Function to load all products
def load_products():
    global row_counter, frame_list, img_list, no_list
    
    # Clear existing products
    for frame in frame_list:
        frame.destroy()
    
    frame_list = []
    img_list = []
    no_list = []
    row_counter = 0
    
    # Get all products from database
    products = get_all_products()
    
    for i, product in enumerate(products):
        # Handle different tuple sizes - we need at least pid, price, name, description
        if len(product) >= 4:
            pid = product[0]
            price = product[1] 
            name = product[2]
            description = product[3]
            # retailer_email might be at index 4 if it exists
        
        # Calculate the number of images for this product
        import os
        product_dir = f"Products/Product {pid}"
        
        if os.path.exists(product_dir):
            image_count = len([file for file in os.listdir(product_dir) if file.endswith('.jpg')])
            no_list.append(image_count if image_count > 0 else 1)
        else:
            no_list.append(1)  # Default to 1 if no directory exists
        
        if i % 3 == 0 and i != 0:
            row_counter += 1

        # Create a nice product card
        frame = tk.Frame(Products_Frame, bg='#282c34', highlightbackground='#3a3f4b', 
                       highlightthickness=1, padx=15, pady=15, width=350, height=400)
        
        frame.grid_propagate(0)  # Prevent shrinking
        frame_list.append(frame)
        frame.grid(row=row_counter, column=i%3, padx=20, pady=20, sticky='nsew')
        
        image_path = f"Products/Product {pid}/1.jpg"
        if not os.path.exists(image_path):
            image_path = "Products/placeholder.jpg"
            
        img = ImageTk.PhotoImage(Image.open(image_path).resize((184,246)))
        img_list.append(img)
        
        # Image in a frame for better alignment
        img_frame = tk.Frame(frame, bg='#282c34')
        img_frame.pack(fill='x', pady=5)
        img_label = Label(img_frame, image=img, style='image.TLabel')
        img_label.pack(anchor='center')
        
        # Product info in a separate frame
        info_frame = tk.Frame(frame, bg='#282c34', pady=5)
        info_frame.pack(fill='x')
        
        name_label = tk.Button(info_frame, text=name, command=lambda pid=pid, img_count=no_list[-1]: viewitem(pid, img_count), 
                            font=('Times New Roman', 12, 'bold'), fg='white', bg='#282c34', bd=0, relief='flat',
                            wraplength=300, justify='center')
        name_label.pack(fill='x')
        
        price_label = tk.Label(info_frame, text='₹' + str(price), font=('Times New Roman', 15, 'bold'), 
                             fg='#fed25f', bg='#282c34')
        price_label.pack(pady=5)
        
        # Only show Add to Cart button for customers
        email = get_email()
        if email != "":
            add_cart_btn = tk.Button(frame, text='🛒 Add to Cart', command=lambda pid=pid: add_to_cart(pid),
                                  bg='#fed25f', fg='black', font=('Times New Roman', 12, 'bold'),
                                  width=15, pady=5)
            add_cart_btn.pack(pady=5)

# Refresh products whenever a retailer adds or edits products
def refresh_products():
    load_products()

# Initial load of products
load_products()

root.mainloop()
