import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def insert_user(user_name, password, user_type):
    sql = 'INSERT INTO ecuser VALUES (default, %s, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name,  hashed_password, salt, user_type))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0 
        
    finally:
        cursor.close()
        connection.close()
        
    return count


def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password


def show_item():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT name, types, price, stock, comments, size FROM product'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def insert_product(name, types, price, stock, comments, size):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO product VALUES (default, %s, %s, %s, %s, %s, %s)'
    cursor.execute(sql, (name, types, price, stock, comments, size))
    connection.commit()
    cursor.close()
    connection.close()
    
def delete_product(name):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'DELETE FROM product WHERE name = %s'
    cursor.execute(sql, (name,))
    connection.commit()
    cursor.close()
    connection.close()
    
def search_products(query):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM product WHERE name LIKE %s'
    cursor.execute(sql, ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
    
def get_product_by_name(product_name):
    connection = get_connection() 
    cursor = connection.cursor()

    sql = 'SELECT * FROM product WHERE name = %s'
    cursor.execute(sql, (product_name,))
    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return product
        
def show_products():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT name, types, price, stock FROM product'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def get_product_by_id(product_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT name, types, price, stock, comments, size FROM product WHERE id = %s"
    cursor.execute(sql, (product_id,))
    product = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return product

def get_products_by_id(product_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = 'SELECT name, price FROM product WHERE id = %s'
    cursor.execute(sql, (product_id,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def add_to_cart(product_id, ecuser_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO cart (product_id, quantity, ecuser_id) VALUES (%s, 1, %s) RETURNING id"

    cursor.execute(sql, (product_id, ecuser_id))
    cart_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()
    return cart_id

def remove_from_cart(product_id, ecuser_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "DELETE FROM cart WHERE product_id = %s AND ecuser_id = %s"

    cursor.execute(sql, (product_id, ecuser_id))

    connection.commit()

    cursor.close()
    connection.close()

def get_cart_items(ecuser_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT c.quantity, p.name, p.price FROM cart c JOIN product p ON c.product_id = p.id WHERE c.ecuser_id = %s"
    cursor.execute(sql, (ecuser_id,))
    cart_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return cart_items

def calculate_cart_total(ecuser_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = 'SELECT SUM(p.price * c.quantity) FROM product p ' \
          'JOIN cart c ON p.id = c.product_id WHERE c.ecuser_id = %s'
    cursor.execute(sql, (ecuser_id,))
    total_price = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total_price

def get_order(ecuser_id, total_price):
    connection = get_connection()
    cursor = connection.cursor()

    # Assuming you have an "orders" table to store the orders with columns like order_id, ecuser_id, total_price, etc.
    sql = 'INSERT INTO orders (ecuser_id, total_price) VALUES (%s, %s) RETURNING order_id'
    cursor.execute(sql, (ecuser_id, total_price))
    order_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return order_id

def get_product_name(product_name):
    sql = 'SELECT id, name, price FROM product WHERE name = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (product_name,))
        product = cursor.fetchone()
        return product
    except psycopg2.DatabaseError:
        return None
    finally:
        cursor.close()
        connection.close()
    
def admin_login(user_name, password):
    sql = 'SELECT password, salt FROM ecuser WHERE user_name = %s AND user_type = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, 'admin'))
        user = cursor.fetchone()
        if user is not None:
            salt = user[1]
            hashed_password = get_hash(password, salt)
            if hashed_password == user[0]:
                return True
    except psycopg2.DatabaseError:
        pass
    finally:
        cursor.close()
        connection.close()
    return False  

def user_login(user_name, password):
    sql = 'SELECT password, salt FROM ecuser WHERE user_name = %s AND user_type = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, 'user'))
        user = cursor.fetchone()
        if user is not None:
            salt = user[1]
            hashed_password = get_hash(password, salt)
            if hashed_password == user[0]:
                return True
    except psycopg2.DatabaseError:
        pass
    finally:
        cursor.close()
        connection.close()
    return False

