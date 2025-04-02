import tkinter as tk 
from tkinter.ttk import *
from db import *
import tkinter.messagebox as messagebox
from PIL import ImageTk,Image
from savedata import *
from otp import *
from cart import *

update_file(False)

def signin():
    style = Style()
    style.configure('signin.TEntry', height = 20, width = 3)
    style.configure('signin_entry.TLabel', background = '#282c34', foreground = 'white', padding = [0,0,0,5], justify = 'left', anchor = 'w')
    style.configure('Heading.TLabel', font = 'Impact 32', background = '#282c34', justify = 'center', foreground = 'white')

    global bg_img
    signin_win = tk.Toplevel()
    signin_win.geometry("581x322")
    signin_win.resizable(False, False)

    # ========== Frames ========== 
    signin_win.configure(bg = '#21252b')

    frame = tk.Frame(signin_win, bg = '#282c34')
    frame.place(x=11, y=11, height = 301, width = 560)
    
    heading = Label(frame, text = 'SIGNIN', style = 'Heading.TLabel')

    # ========== Creating Widgets ========== 
    Fname = Entry(frame, style = 'signin.TEntry')
    Fname_label = Label(frame, text='First name : ', style = 'signin_entry.TLabel')

    Lname = Entry(frame, style = 'signin.TEntry')
    Lname_label = Label(frame, text='Last name : ', style = 'signin_entry.TLabel')

    email = Entry(frame, style = 'signin.TEntry')
    email_label = Label(frame, text='Email id : ', style = 'signin_entry.TLabel')

    password = Entry(frame, style = 'signin.TEntry')
    password_label = Label(frame, text='Password : ', style = 'signin_entry.TLabel')

    otp = Entry(frame, style = 'signin.TEntry')
    otp_label = Label(frame, text='Enter OTP : ', style = 'signin_entry.TLabel')

    resend_otp = tk.Button(frame, text = 'Resend OTP ? ', command = lambda : send_otp(email.get()), bg = 'white', fg = '#219afc', bd = 0)

    t = "* Password must be <20 characters long, have at least 1 upper case character, 1 lower case character, 1 of (@, - or _)"

    Info = tk.Message(frame, bg = '#282c34', text = t, font = ('Times New Roman', 10, 'italic'), fg = '#f7576c', width = 560)

    # ========== Placing Widgets ========== 
    heading.grid(row=0, column=0, columnspan=2)

    Fname_label.grid(row = 1, column = 0)
    Fname.grid(row = 1, column = 1)
    
    Lname_label.grid(row = 2, column = 0)
    Lname.grid(row = 2 , column = 1)
    
    email_label.grid(row = 3, column = 0)
    email.grid(row = 3, column = 1)
    
    password_label.grid(row = 4, column = 0)
    password.grid(row = 4, column = 1)
    
    Info.grid(row = 5, column = 0, columnspan = 2)

    email_var = ''
    data = ()

    def enter():
        global email_var
        global data

        email_var = email.get()
        data = (Fname.get(), Lname.get(), email.get(), password.get())

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

        # Login Successful             
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
            messagebox.showerror("","Password Should have at least 1 upper case character")
        elif special == 0:
            messagebox.showerror("","Password should have at least one @, - or _")
        elif digit == 0:
            messagebox.showerror("","Password should have at least one number")
    
    def otp_func():
        global email_var
        global data
        
        password_list = check_details(email_var)
        
        if len(password_list) == 0:
            send_otp(email_var)
            otp_label.place(x=0, y=59)
            otp.place(x=77, y=59)

            resend_otp.place(x=0, y= 87)

            def check_otp():
                if str(otp.get()) == read_file()[1]:
                    createaccount(data)
                    update_file(True)
                    messagebox.showinfo("","Logged in Successfuly")
                else:
                    messagebox.showerror("","Incorrect OTP")

            btn = Button(frame, text = 'Enter', command =lambda: [check_otp(), signin_win.destroy()])
            btn.place(x=122, y=115)
        else:
            messagebox.showerror("","Email Already in Use")
   
    enter_button = tk.Button(frame, text = 'Enter', command = lambda: [enter(), otp_func()], padx = 5)
    enter_button.grid(row = 6, column = 0, pady = 20, padx = 200, columnspan = 2)

def login(login_state, Account_frame):
    style = Style()
    style.configure('signin.TEntry', height = 20, width = 3)
    style.configure('login_entry.TLabel', background = '#282c34', foreground = 'white', padding = [100,0,0,5], justify = 'left', anchor = 'w')
    style.configure('Heading.TLabel', font = 'Impact 32', background = '#282c34', justify = 'center', foreground = 'white', padding = [200,0,0,5])


    global bg_img
    login_win = tk.Toplevel()
    login_win.geometry("581x322")
    login_win.resizable(False, False)

    # ========== Background and Frames ========== 
    login_win.configure(bg = '#282c34')

    frame = tk.Frame(login_win, bg = '#282c34')
    frame.place(x=11, y=11, height = 301, width = 560)

    # ========== Creating Widgets ========== 
    heading = Label(frame, text = 'LOGIN', style = 'Heading.TLabel')
    heading.grid(row = 0, column = 0, columnspan = 2, sticky = 'we')

    email = Entry(frame, style = 'signin.TEntry')
    email_label = Label(frame, text='Email id : ', style = 'login_entry.TLabel')

    password = Entry(frame, style = 'signin.TEntry')
    password_label = Label(frame, text='Password : ', style = 'login_entry.TLabel')

    otp = Entry(frame, style = 'signin.TEntry')
    otp_label = Label(frame, text='Enter OTP : ', style = 'login_entry.TLabel')

    resend_otp = tk.Button(frame, text = 'Resend OTP ? ', command = lambda : send_otp(email.get()), bg = '#282c34', fg = '#219afc', bd = 0)
    forgotpassword_label = tk.Button(frame, text = 'forgot password ?', command = lambda : forgotpassword(Account_frame), bg = '#282c34', fg = '#219afc', bd = 0, padx = 100)

    # ========== Placing Widgets ========== 
    email_label.grid(row = 1, column = 0, pady = 10)
    email.grid(row = 1, column = 1)
    
    password_label.grid(row = 2, column = 0, pady = 10)
    password.grid(row = 2, column = 1)

    forgotpassword_label.grid(row = 3, column = 0, columnspan = 2, pady = 10)

    def enter(login_state):
        data = (email.get(), password.get())
        password_list = check_details(data[0], data[1])
        
        if len(password_list)>0:
            if data[1] == password_list[0][0]:
                update_file(True)
                create_cart(email.get())
                update_email_file(email.get())
                
                for widgets in Account_frame.winfo_children():
                    widgets.destroy()
            
                cart_button = tk.Button(Account_frame, text='🛒 Cart', command=cart, 
                                      padx=10, pady=5, bg='#3276fc', 
                                      fg='white', font=('Times New Roman', 12, 'bold'))
                logout_button = tk.Button(Account_frame, text='Logout', 
                                        command=lambda: logout(Account_frame),
                                        padx=10, pady=5, bg='#3276fc',
                                        fg='white', font=('Times New Roman', 12, 'bold'))
                
                cart_button.grid(row=0, column=0, padx=5)
                logout_button.grid(row=0, column=1, padx=5)
                
                messagebox.showinfo("","Logged In Successfuly")

            else:
                response = messagebox.showerror("","Incorrect Password")
        else:
            response = messagebox.showerror("","Account Name Doesn't Exist")        

    enter_button = Button(frame, text = 'Enter', command = lambda: [enter(login_state), login_win.destroy()])
    enter_button.grid(row = 4, column = 0, columnspan = 2, padx = 200, pady = 20)


    def forgotpassword(Account_frame):
        email.grid_forget()
        email_label.grid_forget()
        password.grid_forget()
        password_label.grid_forget()
        forgotpassword_label.grid_forget()
        enter_button.grid_forget()
        
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
                            update_password(new_password, email)
                            messagebox.showinfo("","Password changed Successfuly")
                        else:
                            messagebox.showerror("","Both passwords are not same ")

                    # ========== Creating Widgets ========== 
                    new_password_label = Label(frame, text = 'New Password : ', style = 'signin_entry.TLabel')
                    new_password = Entry(frame, style = 'signin.TEntry')
                    re_enter_password_label = Label(frame, text = 'Re-enter Password : ', style = 'signin_entry.TLabel')
                    re_enter_password = Entry(frame, style = 'signin.TEntry')
                    verify_btn = Button(frame, text = 'Verify', style = 'a.TButton', command = lambda: verify(new_password.get(), re_enter_password.get(), email_var))

                    # ========== Placing Widgets ========== 
                    new_password_label.grid(row = 1, column = 0, pady = 10)
                    new_password.grid(row = 1, column = 1)

                    re_enter_password_label.grid(row = 2, column = 0, pady = 10)
                    re_enter_password.grid(row = 2, column = 1)

                    verify_btn.grid(row = 3, column = 0, padx = 200, pady = 20, columnspan = 2)
                else:
                    messagebox.showerror("","Incorrect OTP")

            e_btn = Button(frame, text = 'Enter', style = 'a.TButton', command = otp_func_1)

            otp_label.grid(row = 1, column = 0 , pady = 10)
            otp.grid(row = 1, column = 1)

            e_btn.grid(row = 2, column = 0, pady = 20 , padx = 200, columnspan = 2)
        
        def email_otp():
            global email_var
            email_var = email.get()
            if len(check_details(email_var)) != 0:
                send_otp(email_var)
            else:
                messagebox.showerror("","Email is not registered")


        email_label.grid(row = 1, column = 0, pady = 10)
        email.grid(row = 1, column = 1)

        send_otp_button = Button(frame, text = 'Send OTP', command = lambda : [email_otp(), forget_buttons()], style = 'a.TButton')

        send_otp_button.grid(row = 3, column = 0, pady = 20, padx = 200, columnspan = 2)
        # btn.place(x=90, y=154)

def user_login(Account_frame):
    login_state = read_file()[0]
    login(login_state, Account_frame)

def logout(Account_frame):
    update_file(False)
    update_email_file("")
    
    for widgets in Account_frame.winfo_children():
        widgets.destroy()
        
    signin_button = tk.Button(Account_frame, text='Sign in', padx=10, pady=5, 
                            command=signin, bg='#3276fc', fg='white', 
                            font=('Times New Roman', 12, 'bold'))
    login_button = tk.Button(Account_frame, text='Log in', padx=10, pady=5,
                            command=lambda: login(False, Account_frame), bg='#3276fc', 
                            fg='white', font=('Times New Roman', 12, 'bold'))
    
    signin_button.grid(row=0, column=0, padx=5)
    login_button.grid(row=0, column=1, padx=5)
    
    messagebox.showinfo("","Logged Out Successfully")

# root = tk.Tk()
# signin()
# root.mainloop()