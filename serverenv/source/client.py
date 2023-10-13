import socket  # Importa o módulo socket para criar e gerenciar conexões de rede
import threading # Importa módulo que permite trabalhar com threads 
import sqlite3 # Importa módulo que permite usar banco de dados SQLite
import datetime # Importa módulo para fornecer timestamps
import warnings # importa módulo para suprimir avisos no terminal

# Cria um lock para sincronizar o acesso ao banco de dados
db_lock = threading.Lock()

# Suprime os avisos de DeprecationWarning relacionados ao adaptador de data e hora
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Função para criar a tabela no banco de dados
def create_table():
    # Conecta-se ao banco de dados ou cria um novo arquivo 'database.db' se ele não existir
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Cria uma tabela chamada "temperatura" se ela não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura FLOAT,
            data_hora DATETIME
        )
    """)
    
    # Fecha a conexão com o banco de dados
    conn.close()

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Adquira o bloqueio antes de escrever no banco de dados para evitar conflitos
            with db_lock:
                cursor.execute("INSERT INTO temperatura (temperatura, data_hora) VALUES (?, ?)", (data.decode(), datetime.datetime.now()))
                conn.commit()

            # Fecha a conexão com o banco de dados
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
                \r2 - Mostrar base de dados\n"""

        print(menu)
        opcao = input(">>> ")

        if opcao == '1':
            print("Conexão encerrada")
            client_socket.close()
            break

        elif opcao == '2':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Adquira o bloqueio antes de ler do banco de dados para evitar conflitos
            with db_lock:
                cursor.execute("SELECT * FROM temperatura")
                column_names = [description[0] for description in cursor.description]
                print(column_names)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

            # Fecha a conexão com o banco de dados
            conn.close()

# Função para iniciar o cliente
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

    # Aguarda o término das threads antes de encerrar o programa
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":  # Verifica se este script é o principal e, em caso afirmativo, inicia o cliente
    start_client()
