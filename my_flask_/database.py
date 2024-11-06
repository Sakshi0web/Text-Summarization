# # import sqlite3

# # def create_tables():
# #     conn = sqlite3.connect('user_data.db')
# #     cursor = conn.cursor()
# #     cursor.execute('''
# #         CREATE TABLE IF NOT EXISTS users (
# #             id INTEGER PRIMARY KEY,
# #             username TEXT UNIQUE NOT NULL,
# #             email TEXT UNIQUE NOT NULL,
# #             password TEXT NOT NULL
# #         )
# #     ''')
# #     conn.commit()
# #     conn.close()

# # def add_user(username, email, password):
# #     conn = sqlite3.connect('user_data.db')
# #     cursor = conn.cursor()
# #     cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
# #     conn.commit()
# #     conn.close()

# # def get_user_by_username(username):
# #     conn = sqlite3.connect('user_data.db')
# #     cursor = conn.cursor()
# #     cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
# #     user = cursor.fetchone()
# #     conn.close()
# #     return user


# # import sqlite3

# # # Establish a connection to your SQLite3 database
# # db_connection = sqlite3.connect('users.db')

# # def initialize_database():
# #     cursor = db_connection.cursor()
    
# #     # Create a table to store user information if it doesn't exist
# #     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         username TEXT NOT NULL UNIQUE,
# #         email TEXT NOT NULL,
# #         password TEXT NOT NULL
# #     )''')
    
# #     # Commit changes and close the cursor
# #     db_connection.commit()
# #     cursor.close()


# import sqlite3

# # Establish a connection to your SQLite3 database
# db_connection = sqlite3.connect('users.db')

# def initialize_database():
#     cursor = db_connection.cursor()
    
#     # Create a table to store user information if it doesn't exist
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT NOT NULL UNIQUE,
#         email TEXT NOT NULL,
#         password TEXT NOT NULL
#     )''')
#     pass
    
#     # Commit changes and close the cursor
#     db_connection.commit()
#     cursor.close()

# def add_user(username, email, password):
#     cursor = db_connection.cursor()
#     cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
#     db_connection.commit()
#     pass

# def get_user_by_username(username):
#     cursor = db_connection.cursor()
#     cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
#     user = cursor.fetchone()
#     return user
 
import sqlite3

def initialize_database():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user
