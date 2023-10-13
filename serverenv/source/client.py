import socket
import threading
import sqlite3
import datetime
import warnings

# Cria um lock para sincronizar o acesso ao banco de dados
db_lock = threading.Lock()

warnings.filterwarnings("ignore", category=DeprecationWarning)

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura FLOAT,
            data_hora DATETIME
        )
    """)
    conn.close()

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Adquira o bloqueio antes de escrever no banco de dados
            with db_lock:
                cursor.execute("INSERT INTO temperatura (temperatura, data_hora) VALUES (?, ?)", (data.decode(), datetime.datetime.now()))
                conn.commit()

            conn.close()

            if not data:
                break
        except Exception as e:
            print("Erro: ", str(e))
            break

# Função para mostrar um menu e selecionar opções
def send_options(client_socket):
    while True:
        menu = """\n1 - Encerrar conexão\n
                \r2 - Mostrar base de dados\n
                \r3 - Mostrar gráfico\n"""

        print(menu)
        opcao = input(">>> ")

        if opcao == '1':
            print("Conexão encerrada")
            client_socket.close()
            break

        elif opcao == '2':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Adquira o bloqueio antes de ler do banco de dados
            with db_lock:
                cursor.execute("SELECT * FROM temperatura")
                column_names = [description[0] for description in cursor.description]
                print(column_names)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

            conn.close()

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

    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":
    start_client()
