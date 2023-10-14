import socket  # Import the socket module for creating and managing network connections
import random  # Import the module to provide random numbers
import time  # Import the module with time-related features
import datetime  # Import the module to provide timestamps

def start_server():
    host = 'localhost'  # Host address where the server will be initiated
    port = 5000  # Port where the server will listen

    # Create a new socket using the TCP protocol (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified host and port
    server_socket.bind((host, port))

    # Put the socket in listening mode, waiting for client connections
    server_socket.listen()

    print(f"Server started at {host}:{port}")

    # Accept a new client connection
    conn, addr = server_socket.accept()

    print(f"Connection established with {addr}\n")

    while True:  # Client communication loop
        try:
            # Generate random numbers between 20 and 30, print the value and a timestamp
            random_number = str("{0:.1f}".format(random.uniform(20, 30)))
            print(f"Temperature: {random_number} \t Date: {datetime.datetime.now()}")
            conn.sendall(random_number.encode())  # Send temperature to the client
            # Wait for 1 second
            time.sleep(1)
        except KeyboardInterrupt:
            # Close the connection in case of task cancellation in the terminal using ctrl+c
            print("Connection terminated")
            conn.close()
            break
        except ConnectionResetError:
            # Close the connection if the client cancels the task in the terminal using ctrl+c
            print("Connection terminated")
            conn.close()
            break
        except BrokenPipeError:
            # Close the connection if the client cancels the task in the terminal using ctrl+c
            print("Connection terminated")
            conn.close()
            break

if __name__ == "__main__":  # Check if this script is the main one and, if so, start the server
    start_server()
