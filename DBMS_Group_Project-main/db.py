import mysql.connector as sql

con = sql.connect(host="localhost", user='ks', passwd='password')

c = con.cursor()

def createdb():
    c.execute("CREATE DATABASE IF NOT EXISTS SHOPPING;")

    con.commit()


def createtable():
    c.execute("USE SHOPPING;")
    c.execute("CREATE TABLE IF NOT EXISTS accounts(Fname varchar(30), Lname varchar(30), email varchar(30) primary key, password varchar(30) NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS product(pid integer primary key, price integer NOT NULL, name varchar(255), description varchar(900));")
    c.execute("SELECT * FROM product;")
    if len(c.fetchall()) == 0:
        # insert values into product table
        c.execute("INSERT INTO product VALUES(1, 999, 'Jeansian Mens T-Shirt', 'Short Sleeve ;Dry Fit ;Running ;Fitness ;Workout ;Black');")     
        c.execute("INSERT INTO product VALUES(2, 299, 'Cloth Theory Boys Regular fit Trousers', 'Hand Wash Only ;Regular Color ;Black ;100 percent cotton ;Stylish everyday wear joggers ;Unique Fabric');")
        c.execute("INSERT INTO product VALUES(3, 499, 'IndoPrimo Mens Casual Shirt', 'Hand Wash Only ;Fit Type: Regular Fit ;Breathable fabric: 100% cotton that is what makes our shirt so good. Soft and light on your skin ;Suitable for: Sports, Casual, Business Work, Date, Party ;Perfect gift for families, friends and boyfriend ;Slim Fit ;Fabric: 100% Cotton ;Full Sleeve ;Good Quality and Premium Stitching ;Wash Instruction: Handwash in cold water NO BLEACH, Low iron and tumble dry on low heat Pattern Type: Solid ;Sleeve Type: Long Sleeve ;Collar Style: Round Collar');")
        c.execute("INSERT INTO product VALUES(4, 479, 'As Fashion Mens Half Sleeve Shirt', 'Care Instructions: Dry Clean Only ;Fit Type: Slim Fit ;Made of 100/% Cotton, soft, comfy and breathable. ;Look trendy and feel comfortable with this T Shirt. ;This Shirt will cater a rich in-class and genuine appearance in any kind of ambience and will comfort you with saving time. ;This Shirt is perfect for everyone like school-college student, working and sports person etc. and can be wear in workplaces, house or kitty parties, friendly outings, sports activities or even while travelling. ;Closure Type: Button ;Pattern Type: All Over Print ;Collar Style: Classic Collar ;Sleeve Type: 3/4 Sleeve ;Material Composition: Cotton 100 ;Occasion Type: Evening ;');")
        c.execute("INSERT INTO product VALUES(5, 489, 'Jam & Honey Boys Regular Button Down Shirt', 'Care Instructions: Machine Wash ;Fit Type: Regular ;Full sleeve shirts which can be adjusted with a button ;Material: 100% Cotton ;Number of items: 1 ;');")
        c.execute("INSERT INTO product VALUES(6, 219, 'Istyle Can Casual Womens Crop Top', 'Care Instructions: Hand Wash Only ;Fit Type: Regular ;Fabric : Cotton ;Length : Crop ;Neck Style : Round Neck ;Sleeve Type : Half Sleeve ;Print : Butterfly Print , Beautiful Print , Panda Print , Grass Panda , Meow Print , Grow , OPPS , Crown Cat ;');")
        c.execute("INSERT INTO product VALUES(7, 249, 'Istyle Can Block Womens Top', 'Care Instructions: Machine Wash ;Fit Type: Regular Fit ;Neck : V Neck ;Sleeve Style : Short Sleeve ;Fit : Regular Fit ;Fabric : Polyester ;Pattern : Color Block ;');")
        c.execute("INSERT INTO product VALUES(8, 740, 'SunAndRain Mens Baseball Shirt', 'Turkish Cotton,Jersey ;Pull On closure ;Machine Wash ;100% worlds most famo ;s Turkish Cotton best quality soft fabric maintains long lasting color and fabric quality. Easy care machine washable and dry in low heat dryer ;Fashionable contrast  ;olors three-quarter sleeve raglan baseball shirt comes with round neck, plain and customizable tee ;Wide range color opti ;ns has trendy choice as Black Body-Camo Sleeves or Black Body-Turquoise please see drop-down menu for more beautiful color pick ;Unisex Regular Fit for mens womens teenagers for every age people sizing S to 2XL, everyday essential shirt makes great look and provide comfortable daily wear or at ;letic wear ;Gift idea for Birthdays, Christmas, Anniversary for someone who likes casual wear ;');")
        
    con.commit()


def createaccount(data):
    c.execute("USE SHOPPING;")
    c.execute("INSERT INTO accounts VALUES(%s, %s, %s, %s);", data)

    con.commit()
    

def check_details(email, password = None):
    c.execute("USE SHOPPING;")
    c.execute("SELECT password FROM accounts WHERE email = %s;", (email, ))
    
    d = c.fetchall()
    return d

    con.commit()
    

def get_info(product_number):
    c.execute("USE SHOPPING;")
    c.execute('SELECT * FROM product WHERE pid = %s;', (product_number, ))
    data = c.fetchall()
    return data[0]
    con.commit()

def get_price():
    c.execute("USE SHOPPING;")
    c.execute("SELECT price FROM product ;")
    data = ()

    for i in c.fetchall():
        data += i
    return data


def update_password(new_password, email):
    c.execute("USE SHOPPING;")
    c.execute("UPDATE accounts SET password = %s WHERE email = %s;", (new_password, email))
    con.commit()

def create_cart(email):
    c.execute("USE SHOPPING;")
    c.execute("CREATE TABLE IF NOT EXISTS cart(email varchar(30) primary key, p1 integer, p2 integer, p3 integer, p4 integer, p5 integer, p6 integer, p7 integer, p8 integer, foreign key(email) references accounts(email));")
    c.execute("SELECT * FROM cart WHERE email = %s;", (email, ))
    if len(c.fetchall()) == 0:
        c.execute("INSERT INTO cart VALUES(%s, 0, 0, 0, 0, 0, 0, 0, 0);", (email, ))
    con.commit()

def update_cart(pid, email, num=1):
    c.execute("USE SHOPPING;")
    c.execute("UPDATE cart SET p"+ str(pid) + "= %s where email = %s;", (num, email))
    con.commit()
  
def cart_info():
    c.execute("USE SHOPPING;")
    c.execute("SELECT * FROM cart;")
    data = c.fetchall()
    return data

def clear_cart(email):
    c.execute("USE SHOPPING;")
    c.execute("DELETE FROM cart WHERE email = %s;",(email,))
    c.execute("INSERT INTO cart VALUES(%s, 0, 0, 0, 0, 0, 0, 0, 0);", (email, ))
    con.commit()