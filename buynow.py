import tkinter as tk 
from tkinter.ttk import *
import tkinter.messagebox as messagebox
from db import *
from savedata import *

def buy_now():
    win = tk.Toplevel()
    win.geometry('1200x600')
    win.configure(bg = '#282c34')
    
    style = Style()
    style.configure('buy_now_heading.TLabel', font = 'Impact 32', background = '#282c34', foreground = 'white', width = 52, anchor = 'center')
    style.configure('buy_now_subheading.TLabel', font = 'Impact 24', background = '#282c34', foreground = 'white', width = 52, anchor = 'center')
    style.configure('buy_now_entry.TLabel', font = ('Times New Roman', 12), background = '#282c34', foreground = 'white')
    style.configure('a.TCheckbutton', background = '#282c34', foreground = 'white')
    
    states = [
        'ANDAMAN & NICOBAR ISLANDS',
        'ANDHRA PRADESH',
        'ARUNACHAL PRADESH',
        'ASSAM',
        'BIHAR',
        'CHANDIGARH',
        'CHATTISGARH',
        'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
        'DELHI',
        'GOA',
        'GUJARAT',
        'HARYANA',
        'HIMACHAL PRADESH',
        'JAMMU & KASHMIR',
        'JHARKHAND',
        'KARNATAKA',
        'KERALA',
        'LADAKH',
        'LAKSHADWEEP',
        'MADHYA PRADESH',
        'MAHARASHTRA',
        'MANIPUR',
        'MEGHALAYA',
        'MIZORAM',
        'NAGALAND',
        'ODISHA',
        'PUDUCHERRY',
        'PUNJAB',
        'RAJASTHAN',
        'SIKKIM',
        'TAMIL NADU',
        'TELANGANA',
        'TRIPURA',
        'UTTAR PRADESH',
        'UTTARAKHAND',
        'WEST BENGAL'
    ]
    
    
    def cont():
        mob = Mobile_entry.get()
        pin = Pincode_entry.get()
        
        for widgets in New_adress_frame.winfo_children():
            widgets.destroy()
            
        counter = 0
        
        if len(mob) != 10 and not mob.isdigit():
            messagebox.showerror("","Mobile number should have exactly 10 digits")
            counter = 1
        
        if len(pin) != 6 and not pin.isdigit() and counter == 0:
            messagebox.showerror("","Pincode should have exactly 6 digits")
            
        if counter == 0:
            lbl = tk.Label(New_adress_frame, text = 'Choose Payment Method', font = ('Times New Roman', 14, 'bold'), bg = '#282c34', fg = 'white').pack(pady = 30)
            var = tk.BooleanVar()
            cod = Checkbutton(New_adress_frame, text = 'Cash On Delivery', variable = var, style = 'a.TCheckbutton').pack(pady = 10)
            
            def final():
                if var.get() == 1:
                    messagebox.showinfo('','Order Placed Sucessfully')
                    clear_cart(get_email())
            
            btn = Button(New_adress_frame, text = 'Enter', command = final).pack(pady = 10)       
        
    
    # ========== Creating Widgets ==========
    Heading = Label(win, text = 'Buy now', style = 'buy_now_heading.TLabel')
    
    New_adress_frame = tk.Frame(win, bg = '#282c34')
    create_new_address = Label(New_adress_frame, text = 'Create New Adress', style = 'buy_now_subheading.TLabel')
    
    Country_text = Label(New_adress_frame, text = 'Country/Region', style = 'buy_now_entry.TLabel', state = 'readonly')
    Country_combobox = Combobox(New_adress_frame, value = ['India'])
    
    Name_label = Label(New_adress_frame, text = 'Full Name', style = 'buy_now_entry.TLabel')
    Name_entry = Entry(New_adress_frame)
    
    Mobile = Label(New_adress_frame, text = 'Mobile', style = 'buy_now_entry.TLabel')
    Mobile_entry = Entry(New_adress_frame)
    
    Pincode = Label(New_adress_frame, text ='Pincode', style = 'buy_now_entry.TLabel')
    Pincode_entry = Entry(New_adress_frame)
    
    House = Label(New_adress_frame, text ='Flat,House no., Building, Company, Apartment', style = 'buy_now_entry.TLabel')
    House_entry = Entry(New_adress_frame)
    
    Area = Label(New_adress_frame, text ='Area, Street, Sector, Village', style = 'buy_now_entry.TLabel')
    Area_entry = Entry(New_adress_frame)
    
    Landmark = Label(New_adress_frame, text ='Landmark', style = 'buy_now_entry.TLabel')
    Landmark_entry = Entry(New_adress_frame)
    
    Town = Label(New_adress_frame, text ='Town/City', style = 'buy_now_entry.TLabel')
    Town_entry = Entry(New_adress_frame)
    
    State = Label(New_adress_frame, text ='State', style = 'buy_now_entry.TLabel')
    state_combobox = Combobox(New_adress_frame, value = states, state = 'readonly')
    
    Continue_btn = tk.Button(New_adress_frame, text ='Continue', command = cont)
    
    # ========== Placing Widgets ==========
    Heading.grid(row=0, column=0)
    New_adress_frame.grid(row=2, column=0)
    Country_text.grid(row=0, column=0, padx = 10, pady = 10)
    Country_combobox.grid(row=0, column=1)
    Name_label.grid(row=1, column=0, padx = 10, pady = 10)
    Name_entry.grid(row=1, column=1)
    Mobile.grid(row=2, column=0, padx = 10, pady = 10)
    Mobile_entry.grid(row=2, column=1)
    Pincode.grid(row=3, column=0, padx = 10, pady = 10)
    Pincode_entry.grid(row=3, column=1)
    House.grid(row=4, column=0, padx = 10, pady = 10)
    House_entry.grid(row=4, column=1)
    Area.grid(row=5, column=0, padx = 10, pady = 10)
    Area_entry.grid(row=5, column=1)
    Landmark.grid(row=6, column=0, padx = 10, pady = 10)
    Landmark_entry.grid(row=6, column=1)
    Town.grid(row=7, column=0, padx = 10, pady = 10)
    Town_entry.grid(row=7, column=1)
    State.grid(row=8, column=0, padx = 10, pady = 10)
    state_combobox.grid(row=8, column=1)
    
    Continue_btn.grid(row=9, column=0, padx = 10, pady = 30, columnspan=2)
        
# root = tk.Tk()
# buy_now()
# root.mainloop()