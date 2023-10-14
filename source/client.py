import socket  # Import the socket module for creating and managing network connections
import threading  # Import the module that allows working with threads
import sqlite3  # Import the module for using SQLite databases
import datetime  # Import the module for providing timestamps
import warnings  # Import the module to suppress warnings in the terminal

# Create a lock to synchronize database access
db_lock = threading.Lock()

# Suppress DeprecationWarning related to the datetime adapter
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Function to create a table in the database
def create_table():
    # Connect to the database or create a new file 'database.db' if it doesn't exist
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a table called "temperature" if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature FLOAT,
            date_time DATETIME
        )
    """)

    # Close the database connection
    conn.close()

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Acquire the lock before writing to the database to prevent conflicts
            with db_lock:
                cursor.execute("INSERT INTO temperature (temperature, date_time) VALUES (?, ?)", (data.decode(), datetime.datetime.now()))
                conn.commit()

            # Close the database connection
            conn.close()

            if not data:
                break
        except Exception as e:
            print("Error: ", str(e))
            break

# Function to display a menu and select options
def send_options(client_socket):
    while True:
        menu = """\n1 - Terminate connection\n
                \r2 - Show the database\n"""

        print(menu)
        option = input(">>> ")

        if option == '1':
            print("Connection terminated")
            client_socket.close()
            break

        elif option == '2':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Acquire the lock before reading from the database to prevent conflicts
            with db_lock:
                cursor.execute("SELECT * FROM temperature")
                column_names = [description[0] for description in cursor.description]
                print(column_names)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

            # Close the database connection
            conn.close()

# Function to start the client
def start_client():
    create_table()
    host = 'localhost'
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_options, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    # Wait for the threads to finish before exiting the program
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":  # Check if this script is the main one and, if so, start the client
    start_client()
