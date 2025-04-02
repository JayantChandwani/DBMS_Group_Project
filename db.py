import mysql.connector as sql

con = sql.connect(host="localhost", user='root', passwd='csf212')

c = con.cursor()

def createdb():
    c.execute("CREATE DATABASE IF NOT EXISTS SHOPPING;")
    con.commit()


def fix_email_column_size():
    """Function to recreate tables with correct email column size"""
    c.execute("USE SHOPPING;")

    # First check if tables exist
    c.execute("SHOW TABLES LIKE 'cart';")
    cart_exists = len(c.fetchall()) > 0
    c.execute("SHOW TABLES LIKE 'product';")
    product_exists = len(c.fetchall()) > 0
    c.execute("SHOW TABLES LIKE 'accounts';")
    accounts_exists = len(c.fetchall()) > 0
    c.execute("SHOW TABLES LIKE 'retailers';")
    retailers_exists = len(c.fetchall()) > 0

    if not any([cart_exists, product_exists, accounts_exists, retailers_exists]):
        # If no tables exist, nothing to fix
        return

    # Create temporary tables to store data
    if accounts_exists:
        try:
            c.execute("CREATE TABLE accounts_backup AS SELECT * FROM accounts;")
        except:
            print("Failed to create accounts backup.")
    
    if retailers_exists:
        try:
            c.execute("CREATE TABLE retailers_backup AS SELECT * FROM retailers;")
        except:
            print("Failed to create retailers backup.")
    
    if product_exists:
        try:
            c.execute("CREATE TABLE product_backup AS SELECT * FROM product;")
        except:
            print("Failed to create product backup.")
    
    if cart_exists:
        try:
            c.execute("CREATE TABLE cart_backup AS SELECT * FROM cart;")
        except:
            print("Failed to create cart backup.")

    # Drop tables in correct order to avoid foreign key constraints
    try:
        if cart_exists:
            c.execute("DROP TABLE cart;")
        if product_exists:
            c.execute("DROP TABLE product;")
        if accounts_exists:
            c.execute("DROP TABLE accounts;")
        if retailers_exists:
            c.execute("DROP TABLE retailers;")
    except Exception as e:
        print(f"Error dropping tables: {str(e)}")
        return

    # Recreate tables with correct column sizes
    c.execute("CREATE TABLE IF NOT EXISTS accounts(Fname varchar(30), Lname varchar(30), email varchar(100) primary key, password varchar(30) NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS retailers(Fname varchar(30), Lname varchar(30), email varchar(100) primary key, password varchar(30) NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS product(pid integer primary key AUTO_INCREMENT, price integer NOT NULL, name varchar(255), description varchar(900), retailer_email varchar(100) DEFAULT NULL, FOREIGN KEY (retailer_email) REFERENCES retailers(email) ON DELETE SET NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS cart(email varchar(100) primary key, p1 integer, p2 integer, p3 integer, p4 integer, p5 integer, p6 integer, p7 integer, p8 integer, FOREIGN KEY (email) REFERENCES accounts(email));")
    
    # Restore data from backups
    try:
        if retailers_exists:
            c.execute("INSERT INTO retailers SELECT * FROM retailers_backup;")
    except Exception as e:
        print(f"Error restoring retailers data: {str(e)}")
        
    try:
        if accounts_exists:
            c.execute("INSERT INTO accounts SELECT * FROM accounts_backup;")
    except Exception as e:
        print(f"Error restoring accounts data: {str(e)}")
        
    try:
        if product_exists:
            c.execute("INSERT INTO product SELECT * FROM product_backup;")
    except Exception as e:
        print(f"Error restoring product data: {str(e)}")
        
    try:
        if cart_exists:
            c.execute("INSERT INTO cart SELECT * FROM cart_backup;")
    except Exception as e:
        print(f"Error restoring cart data: {str(e)}")
    
    # Drop backup tables
    try:
        if cart_exists:
            c.execute("DROP TABLE cart_backup;")
        if product_exists:
            c.execute("DROP TABLE product_backup;")
        if accounts_exists:
            c.execute("DROP TABLE accounts_backup;")
        if retailers_exists:
            c.execute("DROP TABLE retailers_backup;")
    except Exception as e:
        print(f"Error dropping backup tables: {str(e)}")
        
    con.commit()


def createtable():
    c.execute("USE SHOPPING;")
    
    # Check if we need to fix the email column size
    try:
        c.execute("SELECT CHARACTER_MAXIMUM_LENGTH FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'SHOPPING' AND TABLE_NAME = 'accounts' AND COLUMN_NAME = 'email';")
        result = c.fetchone()
        if result and result[0] < 100:
            # Column size needs to be fixed
            fix_email_column_size()
    except Exception as e:
        print(f"Error checking column size: {str(e)}")
    
    # Create tables with the correct column sizes
    c.execute("CREATE TABLE IF NOT EXISTS accounts(Fname varchar(30), Lname varchar(30), email varchar(100) primary key, password varchar(30) NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS retailers(Fname varchar(30), Lname varchar(30), email varchar(100) primary key, password varchar(30) NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS product(pid integer primary key AUTO_INCREMENT, price integer NOT NULL, name varchar(255), description varchar(900), retailer_email varchar(100) DEFAULT NULL, FOREIGN KEY (retailer_email) REFERENCES retailers(email) ON DELETE SET NULL);")
    
    # Update cart table structure to support dynamic products
    c.execute("CREATE TABLE IF NOT EXISTS cart_items(id integer primary key AUTO_INCREMENT, email varchar(100), product_id integer, quantity integer DEFAULT 1, FOREIGN KEY (email) REFERENCES accounts(email), FOREIGN KEY (product_id) REFERENCES product(pid));")
    
    # Check if the old cart table exists
    c.execute("SHOW TABLES LIKE 'cart';")
    old_cart_exists = len(c.fetchall()) > 0
    
    # Migrate data from old cart table if it exists
    if old_cart_exists:
        try:
            # Check if cart_items is empty before migration
            c.execute("SELECT COUNT(*) FROM cart_items;")
            cart_items_count = c.fetchone()[0]
            
            if cart_items_count == 0:
                # Get all data from old cart table
                c.execute("SELECT * FROM cart;")
                cart_data = c.fetchall()
                
                # Migrate each non-zero item to the new cart_items table
                for row in cart_data:
                    email = row[0]
                    for i in range(1, 9):  # p1 through p8
                        if row[i] > 0:  # Only migrate non-zero quantities
                            c.execute("INSERT INTO cart_items(email, product_id, quantity) VALUES(%s, %s, %s);", 
                                    (email, i, row[i]))
            
            # Don't drop the old cart table yet to avoid breaking existing code
        except Exception as e:
            print(f"Error migrating cart data: {str(e)}")
    
    # Check if product table is empty and populate default products if needed
    c.execute("SELECT * FROM product;")
    if len(c.fetchall()) == 0:
        # insert values into product table (default products with NULL retailer)
        # Using parameterized queries to handle escaping special characters
        product_data = [
            (1, 999, 'Jeansian Mens T-Shirt', 'Short Sleeve ;Dry Fit ;Running ;Fitness ;Workout ;Black'),
            (2, 299, 'Cloth Theory Boys Regular fit Trousers', 'Hand Wash Only ;Regular Color ;Black ;100 percent cotton ;Stylish everyday wear joggers ;Unique Fabric'),
            (3, 499, 'IndoPrimo Mens Casual Shirt', 'Hand Wash Only ;Fit Type: Regular Fit ;Breathable fabric: 100% cotton that is what makes our shirt so good. Soft and light on your skin ;Suitable for: Sports, Casual, Business Work, Date, Party ;Perfect gift for families, friends and boyfriend ;Slim Fit ;Fabric: 100% Cotton ;Full Sleeve ;Good Quality and Premium Stitching ;Wash Instruction: Handwash in cold water NO BLEACH, Low iron and tumble dry on low heat Pattern Type: Solid ;Sleeve Type: Long Sleeve ;Collar Style: Round Collar'),
            (4, 799, 'Mens Formal Cotton Full Sleeve Shirt', 'Best Quality ;100% Pure Cotton ;Light and Comfortable ;Soothing White Color ;Elite Corporate Look ;Suitable for all seasons'),
            (5, 699, 'JAMKU Cotton Round Neck T-Shirt', 'Made of premium quality lightweight fabric and perfect for Dailywear, Casual Wear ;It comes with round neck and short sleeves featuring a printed design on the chest ;Pattern: Solid ;Wash care: Machine wash, Cold water, Do not bleach ;Fit: Slim'),
            (6, 999, 'Campus Casual Running Shoes', 'Closure: Lace-Up ;Flex: Medium Flex ;Lifestyle: Casual ;Material Type: Mesh ;Warranty Type: Manufacturer ;Ankle Type: Low ankle ;100% original merchandise only ;Comfort level: More ;Secure packaging and hassle free shipping ;This is a Made in India product'),
            (7, 799, 'HRX by Hrithik Roshan Mens Soft Knit Loafers', 'Closure: Slip-on ;Sole Material: Synthetic ;Outer Material: Fabric ;Solid Pattern ;Washcare: Wipe with clean, dry cloth when needed ;Packing: Poly Bag ;Occasion: Casual ;Article Weight: 180 to 240 grams per piece'),
            (8, 399, 'Logitech Wired Gaming G102', 'Connector Type: USB ;Programmable Buttons: 6 ;Indicators: RGB Lights ;Logitech G 102 LIGHTSYNC gaming mouse, USB cable, User documentation, 2-year warranty and Full product support ;Adjustable click force mechanism ;This is a USB-type wired mouse with one 1.83m long cable ;Weight 85g with cable ;Dimensions: 116.6mm x 62.2mm x 38.2mm ;Light Sync RGB ;8000 DPI')
        ]
        
        # Insert products using parameterized queries
        for prod in product_data:
            c.execute("INSERT INTO product(pid, price, name, description) VALUES(%s, %s, %s, %s);", prod)

    con.commit()


def createaccount(data):
    c.execute("USE SHOPPING;")
    c.execute("INSERT INTO accounts VALUES(%s, %s, %s, %s);", data)
    con.commit()


def create_retailer_account(data):
    c.execute("USE SHOPPING;")
    c.execute("INSERT INTO retailers VALUES(%s, %s, %s, %s);", data)
    con.commit()
    

def check_details(email, password = None):
    c.execute("USE SHOPPING;")
    c.execute("SELECT password FROM accounts WHERE email = %s;", (email, ))
    
    d = c.fetchall()
    return d


def check_retailer_details(email, password = None):
    c.execute("USE SHOPPING;")
    c.execute("SELECT password FROM retailers WHERE email = %s;", (email, ))
    
    d = c.fetchall()
    return d


def get_info(product_number):
    c.execute("USE SHOPPING;")
    c.execute('SELECT * FROM product WHERE pid = %s;', (product_number, ))
    data = c.fetchall()
    return data[0]


def update_password(new_password, email):
    c.execute("USE SHOPPING;")
    c.execute("UPDATE accounts SET password = %s WHERE email = %s;", (new_password, email))
    con.commit()


def update_retailer_password(new_password, email):
    c.execute("USE SHOPPING;")
    c.execute("UPDATE retailers SET password = %s WHERE email = %s;", (new_password, email))
    con.commit()


def get_price():
    c.execute("USE SHOPPING;")
    c.execute("SELECT pid, price FROM product ORDER BY pid;")
    results = c.fetchall()
    
    # Create a dictionary with pid as key and price as value
    price_dict = {row[0]: row[1] for row in results}
    
    # For backward compatibility, return a tuple of prices for the first 8 products
    # If a product ID doesn't exist, use 0 as the price
    prices = tuple(price_dict.get(i, 0) for i in range(1, 9))
    return prices


# New function to get price for a specific product
def get_product_price(pid):
    c.execute("USE SHOPPING;")
    c.execute("SELECT price FROM product WHERE pid = %s;", (pid,))
    result = c.fetchone()
    if result:
        return result[0]
    return 0


def create_cart(email):
    c.execute("USE SHOPPING;")
    
    # Check if any cart items exist for this email
    c.execute("SELECT COUNT(*) FROM cart_items WHERE email = %s;", (email,))
    if c.fetchone()[0] == 0:
        # We don't need to create empty entries in advance for cart_items
        # Items are added as needed with update_cart
        return True
    return False


def update_cart(pid, email, num=1):
    c.execute("USE SHOPPING;")
    
    # Check if product exists
    c.execute("SELECT COUNT(*) FROM product WHERE pid = %s;", (pid,))
    if c.fetchone()[0] == 0:
        print(f"Product ID {pid} does not exist.")
        return False
    
    # Check if the item is already in the cart
    c.execute("SELECT id, quantity FROM cart_items WHERE email = %s AND product_id = %s;", (email, pid))
    result = c.fetchone()
    
    if result:
        # Item exists in cart, update quantity
        cart_item_id, current_quantity = result
        if num <= 0:
            # Remove item from cart if quantity is 0 or negative
            c.execute("DELETE FROM cart_items WHERE id = %s;", (cart_item_id,))
        else:
            # Update quantity
            c.execute("UPDATE cart_items SET quantity = %s WHERE id = %s;", (num, cart_item_id))
    else:
        # Item not in cart, insert if quantity > 0
        if num > 0:
            c.execute("INSERT INTO cart_items (email, product_id, quantity) VALUES (%s, %s, %s);", 
                    (email, pid, num))
    
    con.commit()
    return True


def cart_info():
    c.execute("USE SHOPPING;")
    
    # Get all unique emails that have cart items
    c.execute("SELECT DISTINCT email FROM cart_items;")
    emails = c.fetchall()
    
    cart_data = []
    
    for email_row in emails:
        email = email_row[0]
        
        # Get all cart items for this email
        c.execute("""
            SELECT ci.email, ci.product_id, ci.quantity 
            FROM cart_items ci
            WHERE ci.email = %s
            ORDER BY ci.product_id
        """, (email,))
        
        items = c.fetchall()
        
        # Start with just the email
        user_cart = [email]
        
        # Create a dictionary to map product_id to quantity
        product_quantities = {item[1]: item[2] for item in items}
        
        # For backward compatibility, populate p1-p8 quantities
        for i in range(1, 9):
            user_cart.append(product_quantities.get(i, 0))
        
        cart_data.append(tuple(user_cart))
    
    return cart_data


def clear_cart(email):
    c.execute("USE SHOPPING;")
    c.execute("DELETE FROM cart_items WHERE email = %s;", (email,))
    con.commit()


def add_product(name, price, description, retailer_email):
    c.execute("USE SHOPPING;")
    c.execute("INSERT INTO product(name, price, description, retailer_email) VALUES(%s, %s, %s, %s);", 
             (name, price, description, retailer_email))
    # Get the last inserted ID
    c.execute("SELECT LAST_INSERT_ID();")
    pid = c.fetchone()[0]
    con.commit()
    return pid


def update_product(pid, name, price, description, retailer_email):
    c.execute("USE SHOPPING;")
    # Make sure retailer can only update their own products
    c.execute("UPDATE product SET name=%s, price=%s, description=%s WHERE pid=%s AND retailer_email=%s;", 
             (name, price, description, pid, retailer_email))
    affected = c.rowcount
    con.commit()
    return affected > 0


def delete_product(pid, retailer_email):
    c.execute("USE SHOPPING;")
    # Make sure retailer can only delete their own products
    c.execute("DELETE FROM product WHERE pid=%s AND retailer_email=%s;", (pid, retailer_email))
    affected = c.rowcount
    con.commit()
    return affected > 0


def get_retailer_products(retailer_email):
    c.execute("USE SHOPPING;")
    c.execute("SELECT * FROM product WHERE retailer_email=%s;", (retailer_email,))
    data = c.fetchall()
    return data


def get_all_products():
    c.execute("USE SHOPPING;")
    c.execute("SELECT * FROM product;")
    data = c.fetchall()
    return data