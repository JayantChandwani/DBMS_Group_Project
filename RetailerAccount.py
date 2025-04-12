import tkinter as tk 
from tkinter.ttk import *
from db import *
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from savedata import *
from otp import *

# File to track retailer login state
def update_retailer_file(login_state, otp=None):
    data = [login_state, otp]
    with open('retailer_state.txt', 'w') as retailer_file:
        json.dump(data, retailer_file)

def read_retailer_file():
    try:
        with open('retailer_state.txt') as retailer_file:
            data = json.load(retailer_file)
            return data
    except FileNotFoundError:
        # Create the file if it doesn't exist
        update_retailer_file(False)
        return [False, None]

def update_retailer_email_file(email):
    with open('retailer_email_file.txt', 'w') as email_file:
        json.dump(email, email_file)

def get_retailer_email():
    try:
        with open('retailer_email_file.txt') as email_file:
            return json.load(email_file)
    except FileNotFoundError:
        # Create the file if it doesn't exist
        update_retailer_email_file("")
        return ""

# Initialize files
update_retailer_file(False)
update_retailer_email_file("")

def retailer_signin():
    style = Style()
    style.configure('signin.TEntry', height=20, width=3)
    style.configure('signin_entry.TLabel', background='#282c34', foreground='white', padding=[0,0,0,5], justify='left', anchor='w')
    style.configure('Heading.TLabel', font='Impact 32', background='#282c34', justify='center', foreground='white')

    signin_win = tk.Toplevel()
    signin_win.geometry("581x322")
    signin_win.resizable(False, False)
    signin_win.title("Retailer Sign Up")

    # Frames
    signin_win.configure(bg='#21252b')
    frame = tk.Frame(signin_win, bg='#282c34')
    frame.place(x=11, y=11, height=301, width=560)
    
    heading = Label(frame, text='RETAILER SIGNUP', style='Heading.TLabel')

    # Creating Widgets
    Fname = Entry(frame, style='signin.TEntry')
    Fname_label = Label(frame, text='First name : ', style='signin_entry.TLabel')

    Lname = Entry(frame, style='signin.TEntry')
    Lname_label = Label(frame, text='Last name : ', style='signin_entry.TLabel')

    email = Entry(frame, style='signin.TEntry')
    email_label = Label(frame, text='Email id : ', style='signin_entry.TLabel')

    password = Entry(frame, style='signin.TEntry', show="*")
    password_label = Label(frame, text='Password : ', style='signin_entry.TLabel')

    otp = Entry(frame, style='signin.TEntry')
    otp_label = Label(frame, text='Enter OTP : ', style='signin_entry.TLabel')

    resend_otp = tk.Button(frame, text='Resend OTP ? ', command=lambda: send_otp(email.get()), bg='white', fg='#219afc', bd=0)

    t = "* Password must be <20 characters long, have at least 1 upper case character, 1 lower case character, 1 of (@, - or _)"
    Info = tk.Message(frame, bg='#282c34', text=t, font=('Times New Roman', 10, 'italic'), fg='#f7576c', width=560)

    # Placing Widgets
    heading.grid(row=0, column=0, columnspan=2)
    Fname_label.grid(row=1, column=0)
    Fname.grid(row=1, column=1)
    Lname_label.grid(row=2, column=0)
    Lname.grid(row=2, column=1)
    email_label.grid(row=3, column=0)
    email.grid(row=3, column=1)
    password_label.grid(row=4, column=0)
    password.grid(row=4, column=1)
    Info.grid(row=5, column=0, columnspan=2)

    email_var = ''
    data = ()

    def enter():
        nonlocal email_var, data
        email_var = email.get()
        data = (Fname.get(), Lname.get(), email.get(), password.get())

        # Password validation
        upper = 0
        special = 0
        digit = 0

        if email.get().split("@")[1] in ['gmail.com']:
            if len(password.get()) <= 20:
                for i in password.get():
                    if i.isupper():
                        upper = 1
                    if i in ('@', "-", "_"):
                        special = 1
                    if i.isdigit():
                        digit = 1

        # Validation successful
        if upper == 1 and special == 1 and digit == 1:
            Fname_label.grid_forget()
            Lname_label.grid_forget()
            email_label.grid_forget()
            password_label.grid_forget()
            enter_button.grid_forget()
            Info.grid_forget()
            Fname.grid_forget()
            Lname.grid_forget()
            email.grid_forget()
            password.grid_forget()
        elif upper == 0:
            messagebox.showerror("", "Password Should have at least 1 upper case character")
        elif special == 0:
            messagebox.showerror("", "Password should have at least one @, - or _")
        elif digit == 0:
            messagebox.showerror("", "Password should have at least one number")
    
    def otp_func():
        nonlocal email_var, data
        
        # Check if email already used for retailer account
        retailer_password_list = check_retailer_details(email_var)
        
        if len(retailer_password_list) == 0:
            send_otp(email_var)
            otp_label.place(x=0, y=59)
            otp.place(x=77, y=59)
            resend_otp.place(x=0, y=87)

            def check_otp():
                if str(otp.get()) == read_file()[1]:
                    create_retailer_account(data)
                    update_retailer_file(True)
                    update_retailer_email_file(email_var)
                    messagebox.showinfo("", "Retailer Account Created Successfully")
                else:
                    messagebox.showerror("", "Incorrect OTP")

            btn = Button(frame, text='Enter', command=lambda: [check_otp(), signin_win.destroy()])
            btn.place(x=122, y=115)
        else:
            messagebox.showerror("", "Email Already in Use for a Retailer Account")
   
    enter_button = tk.Button(frame, text='Enter', command=lambda: [enter(), otp_func()], padx=5)
    enter_button.grid(row=6, column=0, pady=20, padx=200, columnspan=2)

def retailer_login(Retailer_frame, Account_frame):
    style = Style()
    style.configure('signin.TEntry', height=20, width=3)
    style.configure('login_entry.TLabel', background='#282c34', foreground='white', padding=[100,0,0,5], justify='left', anchor='w')
    style.configure('Heading.TLabel', font='Impact 32', background='#282c34', justify='center', foreground='white', padding=[200,0,0,5])

    login_win = tk.Toplevel()
    login_win.geometry("581x322")
    login_win.resizable(False, False)
    login_win.title("Retailer Login")

    # Background and Frames
    login_win.configure(bg='#282c34')
    frame = tk.Frame(login_win, bg='#282c34')
    frame.place(x=11, y=11, height=301, width=560)

    # Creating Widgets
    heading = Label(frame, text='RETAILER LOGIN', style='Heading.TLabel')
    heading.grid(row=0, column=0, columnspan=2, sticky='we')

    email = Entry(frame, style='signin.TEntry')
    email_label = Label(frame, text='Email id : ', style='login_entry.TLabel')

    password = Entry(frame, style='signin.TEntry', show="*")
    password_label = Label(frame, text='Password : ', style='login_entry.TLabel')

    forgotpassword_label = tk.Button(frame, text='forgot password ?', 
                                   command=lambda: retailer_forgotpassword(Retailer_frame, frame, email, email_label, password, password_label, forgotpassword_label, enter_button), 
                                   bg='#282c34', fg='#219afc', bd=0, padx=100)

    # Placing Widgets
    email_label.grid(row=1, column=0, pady=10)
    email.grid(row=1, column=1)
    
    password_label.grid(row=2, column=0, pady=10)
    password.grid(row=2, column=1)

    forgotpassword_label.grid(row=3, column=0, columnspan=2, pady=10)

    def enter():
        data = (email.get(), password.get())
        password_list = check_retailer_details(data[0])
        
        if len(password_list) > 0:
            if data[1] == password_list[0][0]:
                update_retailer_file(True)
                update_retailer_email_file(data[0])
                
                # Update retailer frame with management options
                for widgets in Retailer_frame.winfo_children():
                    widgets.destroy()

                for widgets in Account_frame.winfo_children():
                    widgets.destroy()
            
                manage_products_button = tk.Button(Retailer_frame, text='Manage Products', 
                                               command=open_product_management, 
                                               padx=10, pady=10, bg='#3276fc', 
                                               fg='white', font='Impact')
                logout_button = tk.Button(Retailer_frame, text='Logout', 
                                       command=lambda: retailer_logout(Retailer_frame),
                                       padx=10, pady=10, bg='#3276fc',
                                       fg='white', font='Impact')
                
                manage_products_button.grid(row=0, column=0, padx=1)
                logout_button.grid(row=0, column=1, padx=1)
                
                messagebox.showinfo("", "Logged In Successfully as Retailer")
            else:
                messagebox.showerror("", "Incorrect Password")
        else:
            messagebox.showerror("", "Retailer Account Doesn't Exist")        

    enter_button = Button(frame, text='Enter', command=lambda: [enter(), login_win.destroy()])
    enter_button.grid(row=4, column=0, columnspan=2, padx=200, pady=20)

def retailer_forgotpassword(Retailer_frame, frame, email, email_label, password, password_label, forgotpassword_label, enter_button):
    # Hide existing widgets
    email_label.grid_forget()
    email.grid_forget()
    password.grid_forget()
    password_label.grid_forget()
    forgotpassword_label.grid_forget()
    enter_button.grid_forget()
    
    style = Style()
    style.configure('signin_entry.TLabel', background='#282c34', foreground='white', padding=[0,0,0,5], justify='left', anchor='w')
    
    email_label = Label(frame, text='Email id : ', style='signin_entry.TLabel')
    email = Entry(frame, style='signin.TEntry')
    otp = Entry(frame, style='signin.TEntry')
    otp_label = Label(frame, text='Enter OTP : ', style='signin_entry.TLabel')
    
    email_var = ''
    
    def forget_buttons():
        email_label.grid_forget()
        email.grid_forget()
        send_otp_button.grid_forget()

        # Function to update frame 
        def otp_func_1():
            if read_file()[1] == otp.get():
                e_btn.grid_forget()
                otp.grid_forget()
                otp_label.grid_forget()

                # Function to verify password and update database
                def verify(new_password, re_enter_password, email):
                    if new_password == re_enter_password:
                        update_retailer_password(new_password, email)
                        messagebox.showinfo("", "Password changed Successfully")
                    else:
                        messagebox.showerror("", "Both passwords are not same")

                # Creating Widgets
                new_password_label = Label(frame, text='New Password : ', style='signin_entry.TLabel')
                new_password = Entry(frame, style='signin.TEntry', show="*")
                re_enter_password_label = Label(frame, text='Re-enter Password : ', style='signin_entry.TLabel')
                re_enter_password = Entry(frame, style='signin.TEntry', show="*")
                verify_btn = Button(frame, text='Verify', command=lambda: verify(new_password.get(), re_enter_password.get(), email_var))

                # Placing Widgets
                new_password_label.grid(row=1, column=0, pady=10)
                new_password.grid(row=1, column=1)
                re_enter_password_label.grid(row=2, column=0, pady=10)
                re_enter_password.grid(row=2, column=1)
                verify_btn.grid(row=3, column=0, padx=200, pady=20, columnspan=2)
            else:
                messagebox.showerror("", "Incorrect OTP")

        e_btn = Button(frame, text='Enter', command=otp_func_1)
        otp_label.grid(row=1, column=0, pady=10)
        otp.grid(row=1, column=1)
        e_btn.grid(row=2, column=0, pady=20, padx=200, columnspan=2)
    
    def email_otp():
        nonlocal email_var
        email_var = email.get()
        if len(check_retailer_details(email_var)) != 0:
            send_otp(email_var)
            forget_buttons()
        else:
            messagebox.showerror("", "Email is not registered as a retailer")

    email_label.grid(row=1, column=0, pady=10)
    email.grid(row=1, column=1)
    send_otp_button = Button(frame, text='Send OTP', command=email_otp)
    send_otp_button.grid(row=3, column=0, pady=20, padx=200, columnspan=2)

def retailer_logout(Retailer_frame):
    update_retailer_file(False)
    update_retailer_email_file("")
    
    for widgets in Retailer_frame.winfo_children():
        widgets.destroy()
        
    retailer_signin_button = tk.Button(Retailer_frame, text='Retailer Sign up', padx=10, pady=10, 
                                    command=retailer_signin, bg='#3276fc', fg='white', font='Impact')
    retailer_login_button = tk.Button(Retailer_frame, text='Retailer Login', padx=10, pady=10,
                                   command=lambda: retailer_login(Retailer_frame), bg='#3276fc', 
                                   fg='white', font='Impact')
    signin_button = tk.Button(Account_frame, text='Sign in', padx=10, pady=5, 
                            command=signin, bg='#3276fc', fg='white', 
                            font=('Times New Roman', 12, 'bold'))
    login_button = tk.Button(Account_frame, text='Log in', padx=10, pady=5,
                            command=lambda: login(False, Account_frame), bg='#3276fc', 
                            fg='white', font=('Times New Roman', 12, 'bold'))
    
    retailer_signin_button.grid(row=0, column=0, padx=1)
    retailer_login_button.grid(row=0, column=1, padx=1)
    signin_button.grid(row=0, column=0, padx=5)
    login_button.grid(row=0, column=1, padx=5)
    
    messagebox.showinfo("", "Logged Out Successfully")

def open_product_management():
    retailer_email = get_retailer_email()
    if retailer_email == "":
        messagebox.showerror("", "You must be logged in as a retailer to manage products")
        return
        
    win = tk.Toplevel()
    win.geometry("1000x700")
    win.title("Product Management")
    win.configure(bg='#282c34')
    
    # Add a header
    header_frame = tk.Frame(win, bg='#282c34', height=60)
    header_frame.pack(fill='x', padx=20, pady=10)
    
    header_label = Label(header_frame, text="Product Management", 
                        font=('Impact', 28), background='#282c34', foreground='white')
    header_label.pack(side='left')
    
    # Divider - use tk.Frame instead of ttk.Frame for bg color
    divider = tk.Frame(win, height=2, bg='#3a3f4b')
    divider.pack(fill='x', padx=20, pady=5)
    
    # Create Notebook for tabbed interface
    style = Style()
    style.configure('TNotebook', background='#282c34', borderwidth=0)
    style.configure('TNotebook.Tab', background='#3276fc', foreground='white', 
                   padding=[20, 5], font=('Times New Roman', 12, 'bold'))
    style.map('TNotebook.Tab', background=[('selected', '#fed25f')], 
             foreground=[('selected', 'black')])
    
    notebook = Notebook(win)
    notebook.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Create frames for each tab
    add_frame = tk.Frame(notebook, bg='#282c34')
    view_frame = tk.Frame(notebook, bg='#282c34')
    
    notebook.add(add_frame, text="Add New Product")
    notebook.add(view_frame, text="View/Edit My Products")
    
    # ========== Add Product Tab ==========
    style.configure('product_label.TLabel', background='#282c34', foreground='white', 
                  font=('Times New Roman', 12), padding=[5, 5])
    style.configure('product_heading.TLabel', background='#282c34', foreground='white', 
                   font=('Impact', 24), padding=[0, 10])
    
    # Create a centered container for the form
    add_container = tk.Frame(add_frame, bg='#282c34', padx=20, pady=20)
    add_container.pack(expand=True, fill='both')
    
    add_heading = Label(add_container, text="Add New Product", style='product_heading.TLabel')
    add_heading.grid(row=0, column=0, columnspan=2, pady=20, sticky='w')
    
    # Create a frame with border for the form
    form_frame = tk.Frame(add_container, bg='#282c34', highlightbackground='#3a3f4b',
                        highlightthickness=1, padx=30, pady=30)
    form_frame.grid(row=1, column=0, sticky='nsew')
    add_container.columnconfigure(0, weight=1)
    
    name_label = Label(form_frame, text="Product Name:", style='product_label.TLabel')
    name_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    name_entry = Entry(form_frame, width=50, font=('Times New Roman', 12))
    name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    
    price_label = Label(form_frame, text="Price (₹):", style='product_label.TLabel')
    price_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)
    price_entry = Entry(form_frame, width=15, font=('Times New Roman', 12))
    price_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    
    desc_label = Label(form_frame, text="Description:", style='product_label.TLabel')
    desc_label.grid(row=2, column=0, sticky='nw', padx=10, pady=10)
    desc_text = tk.Text(form_frame, width=50, height=10, font=('Times New Roman', 12),
                      bg='#21252b', fg='white')
    desc_text.grid(row=2, column=1, padx=10, pady=10, sticky='w')
    
    desc_info = Label(form_frame, text="Use semicolons (;) to separate description points", 
                     style='product_label.TLabel', foreground="#f7576c")
    desc_info.grid(row=3, column=1, sticky='w', padx=10)
    
    def add_product_action():
        name = name_entry.get()
        try:
            price = int(price_entry.get())
        except ValueError:
            messagebox.showerror("", "Price must be a number")
            return
            
        description = desc_text.get("1.0", "end-1c")
        
        if not name or not description or price <= 0:
            messagebox.showerror("", "All fields must be filled correctly")
            return
            
        # Add to database
        new_pid = add_product(name, price, description, retailer_email)
        
        # Create directory for product images
        try:
            import os
            os.makedirs(f"Products/Product {new_pid}", exist_ok=True)
            # Add a placeholder image
            placeholder_path = "Products/placeholder.jpg"
            if not os.path.exists(placeholder_path):
                # Create a blank image
                from PIL import Image
                img = Image.new('RGB', (184, 246), color='gray')
                img.save(placeholder_path)
            
            # Copy placeholder to product folder
            import shutil
            shutil.copy(placeholder_path, f"Products/Product {new_pid}/1.jpg")
            
            messagebox.showinfo("", f"Product added successfully with ID: {new_pid}\n\nPlease add product images to Products/Product {new_pid}/ folder")
            
            # Clear form
            name_entry.delete(0, 'end')
            price_entry.delete(0, 'end')
            desc_text.delete("1.0", "end")
            
            # Refresh product list
            load_products()
            
        except Exception as e:
            messagebox.showerror("", f"Error creating product directory: {str(e)}")
    
    # Button container for alignment
    button_frame = tk.Frame(form_frame, bg='#282c34', pady=10)
    button_frame.grid(row=4, column=1, sticky='e', padx=10, pady=20)
    
    add_button = tk.Button(button_frame, text="Add Product", 
                         command=add_product_action, bg='#fed25f', fg='black',
                         font=('Times New Roman', 12, 'bold'), padx=20, pady=8)
    add_button.pack()
    
    # ========== View/Edit Products Tab ==========
    # Create a container with padding
    view_container = tk.Frame(view_frame, bg='#282c34', padx=20, pady=20)
    view_container.pack(expand=True, fill='both')
    
    view_heading = Label(view_container, text="My Products", style='product_heading.TLabel')
    view_heading.pack(anchor='w', padx=10, pady=10)
    
    # Frame with border for products list
    products_outer_frame = tk.Frame(view_container, bg='#282c34', highlightbackground='#3a3f4b',
                                  highlightthickness=1, padx=20, pady=20)
    products_outer_frame.pack(fill='both', expand=True)
    
    products_canvas = tk.Canvas(products_outer_frame, bg='#282c34', bd=0, highlightthickness=0)
    products_canvas.pack(side='left', fill='both', expand=True)
    
    # Create scrollbar
    yscroll = Scrollbar(products_outer_frame, orient='vertical', command=products_canvas.yview)
    yscroll.pack(side='right', fill='y')
    
    # Configure canvas
    products_canvas.configure(yscrollcommand=yscroll.set)
    products_canvas.bind('<Configure>', lambda e: products_canvas.configure(scrollregion=products_canvas.bbox("all")))
    
    # Create a frame for products
    products_container = tk.Frame(products_canvas, bg='#282c34')
    products_canvas.create_window((0,0), window=products_container, anchor='nw')
    
    def load_products():
        # Clear existing widgets
        for widget in products_container.winfo_children():
            widget.destroy()
            
        # Fetch retailer's products
        products = get_retailer_products(retailer_email)
        
        if not products:
            no_products = Label(products_container, text="You haven't added any products yet.", 
                               foreground='white', background='#282c34', font=('Times New Roman', 14))
            no_products.pack(pady=50)
            return
            
        # Products listing
        for i, product in enumerate(products):
            # Handle different tuple sizes
            if len(product) >= 4:
                pid = product[0]
                price = product[1] 
                name = product[2]
                description = product[3]
                # retailer_email might be at index 4 if it exists
            
            # Create a frame for each product
            product_frame = tk.Frame(products_container, bg='#282c34', highlightbackground='#3a3f4b', 
                                   highlightthickness=1, padx=20, pady=15, width=800)
            product_frame.pack(fill='x', padx=10, pady=10)
            
            # Left side for product details
            details_frame = tk.Frame(product_frame, bg='#282c34')
            details_frame.pack(side='left', fill='x', expand=True)
            
            # Product info
            pid_label = Label(details_frame, text=f"ID: {pid}", style='product_label.TLabel')
            pid_label.grid(row=0, column=0, sticky='w', pady=2)
            
            name_label = Label(details_frame, text=f"Name: {name}", style='product_label.TLabel')
            name_label.grid(row=1, column=0, sticky='w', pady=2)
            
            price_label = Label(details_frame, text=f"Price: ₹{price}", style='product_label.TLabel')
            price_label.grid(row=2, column=0, sticky='w', pady=2)
            
            desc_short = description[:50] + "..." if len(description) > 50 else description
            desc_label = Label(details_frame, text=f"Description: {desc_short}", style='product_label.TLabel')
            desc_label.grid(row=3, column=0, sticky='w', pady=2)
            
            # Right side for buttons
            buttons_frame = tk.Frame(product_frame, bg='#282c34')
            buttons_frame.pack(side='right', padx=10)
            
            edit_button = tk.Button(buttons_frame, text="Edit", 
                                  command=lambda p=product: open_edit_product(p),
                                  bg='#3276fc', fg='white', font=('Times New Roman', 11, 'bold'),
                                  padx=15, pady=5)
            edit_button.pack(pady=5)
            
            delete_button = tk.Button(buttons_frame, text="Delete", 
                                    command=lambda p_id=pid: delete_product_action(p_id),
                                    bg='#f7576c', fg='white', font=('Times New Roman', 11, 'bold'),
                                    padx=15, pady=5)
            delete_button.pack(pady=5)
    
    def delete_product_action(pid):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
        if confirm:
            success = delete_product(pid, retailer_email)
            if success:
                messagebox.showinfo("", "Product deleted successfully")
                load_products()  # Refresh the list
            else:
                messagebox.showerror("", "Failed to delete product")
    
    def open_edit_product(product):
        # Handle different tuple sizes
        if len(product) >= 4:
            pid = product[0]
            price = product[1] 
            name = product[2]
            description = product[3]
            # retailer_email might be at index 4 if it exists
        
        edit_win = tk.Toplevel()
        edit_win.geometry("800x600")
        edit_win.title(f"Edit Product #{pid}")
        edit_win.configure(bg='#282c34')
        
        # Header
        edit_header = tk.Frame(edit_win, bg='#282c34', height=60)
        edit_header.pack(fill='x', padx=20, pady=10)
        
        edit_heading = Label(edit_header, text=f"Edit Product: {name}", 
                           font=('Impact', 24), background='#282c34', foreground='white')
        edit_heading.pack(side='left')
        
        # Divider
        edit_divider = tk.Frame(edit_win, height=2, bg='#3a3f4b')
        edit_divider.pack(fill='x', padx=20, pady=5)
        
        # Content container
        edit_container = tk.Frame(edit_win, bg='#282c34', padx=30, pady=20)
        edit_container.pack(fill='both', expand=True)
        
        # Form in a bordered frame
        edit_form = tk.Frame(edit_container, bg='#282c34', highlightbackground='#3a3f4b',
                           highlightthickness=1, padx=30, pady=30)
        edit_form.pack(fill='both', expand=True)
        
        name_label = Label(edit_form, text="Product Name:", style='product_label.TLabel')
        name_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        name_entry = Entry(edit_form, width=50, font=('Times New Roman', 12))
        name_entry.insert(0, name)
        name_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        price_label = Label(edit_form, text="Price (₹):", style='product_label.TLabel')
        price_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)
        price_entry = Entry(edit_form, width=15, font=('Times New Roman', 12))
        price_entry.insert(0, price)
        price_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        desc_label = Label(edit_form, text="Description:", style='product_label.TLabel')
        desc_label.grid(row=3, column=0, sticky='nw', padx=10, pady=10)
        desc_text = tk.Text(edit_form, width=50, height=10, font=('Times New Roman', 12),
                         bg='#21252b', fg='white')
        desc_text.insert("1.0", description)
        desc_text.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        desc_info = Label(edit_form, text="Use semicolons (;) to separate description points", 
                        style='product_label.TLabel', foreground="#f7576c")
        desc_info.grid(row=4, column=1, sticky='w', padx=10)
        
        def update_product_action():
            new_name = name_entry.get()
            try:
                new_price = int(price_entry.get())
            except ValueError:
                messagebox.showerror("", "Price must be a number")
                return
                
            new_description = desc_text.get("1.0", "end-1c")
            
            if not new_name or not new_description or new_price <= 0:
                messagebox.showerror("", "All fields must be filled correctly")
                return
                
            # Update in database
            success = update_product(pid, new_name, new_price, new_description, retailer_email)
            
            if success:
                messagebox.showinfo("", "Product updated successfully")
                edit_win.destroy()
                load_products()  # Refresh the list
            else:
                messagebox.showerror("", "Failed to update product")
        
        # Button container
        button_container = tk.Frame(edit_form, bg='#282c34')
        button_container.grid(row=5, column=0, columnspan=2, pady=20, sticky='e')
        
        update_button = tk.Button(button_container, text="Update Product", 
                                command=update_product_action, bg='#fed25f', fg='black',
                                font=('Times New Roman', 12, 'bold'), padx=15, pady=8)
        update_button.pack(side='right', padx=10)
        
        cancel_button = tk.Button(button_container, text="Cancel", 
                               command=edit_win.destroy, bg='#3a3f4b', fg='white',
                               font=('Times New Roman', 12), padx=15, pady=8)
        cancel_button.pack(side='right', padx=10)
    
    # Load products initially
    load_products()

# Function to initialize retailer frame
def init_retailer_frame(Retailer_frame, Account_frame):
    retailer_signin_button = tk.Button(Retailer_frame, text='Retailer Sign up', padx=10, pady=5, 
                                    command=retailer_signin, bg='#3276fc', fg='white', 
                                    font=('Times New Roman', 12, 'bold'))
    retailer_login_button = tk.Button(Retailer_frame, text='Retailer Login', padx=10, pady=5,
                                   command=lambda: retailer_login(Retailer_frame, Account_frame), bg='#3276fc', 
                                   fg='white', font=('Times New Roman', 12, 'bold'))
    
    retailer_signin_button.grid(row=0, column=0, padx=5)
    retailer_login_button.grid(row=0, column=1, padx=5) 