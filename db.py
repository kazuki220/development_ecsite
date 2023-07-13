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


def show_products():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM product'
    
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
    
def show_product():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM product WHERE id = ?'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def get_order(ecuser_id, total_price):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM orders'
    
    cursor.execute(sql,(ecuser_id, total_price))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows
    
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

