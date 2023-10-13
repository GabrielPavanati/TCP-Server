import socket  # Importa o módulo socket para criar e gerenciar conexões de rede
import random
import time
import datetime

def start_server():
    host = 'localhost'  # Endereço do host onde o servidor será iniciado
    port = 5000         # Porta onde o servidor estará escutando

    # Cria um novo socket usando o protocolo TCP (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula o socket ao host e porta especificados
    server_socket.bind((host, port))

    # Coloca o socket em modo de escuta, aguardando conexões de clientes
    server_socket.listen()

    print(f"Servidor iniciado em {host}:{port}")

    # Aceita uma nova conexão de cliente
    conn, addr = server_socket.accept()

    print(f"Conexão estabelecida com {addr}\n")

    while True:  # Loop de comunicação com o cliente
        try:
            # Gera números aleatórios entre 20 e 30, imprimindo tal valor e um timestamp
            random_number = str("{0:.1f}".format(random.uniform(20, 30)))
            print(f"Temperatura: {random_number} \t Data: {datetime.datetime.now()}")
            conn.sendall(random_number.encode()) # Envia temperatura para o cliente
            # Aguarda 1 segundo
            time.sleep(1)
        except KeyboardInterrupt:
            # Fecha a conexão em caso de cancelamento da tarefa no terminal, por meio do comando ctrl+c
            print("Conexão encerrada")
            conn.close()
            break
        except ConnectionResetError:
            # Fecha a conexão caso o cliente cancele a tarefa no terminal, por meio do comando ctrl+c
            print("Conexão encerrada")
            conn.close()
            break

if __name__ == "__main__":  # Verifica se este script é o principal e, em caso afirmativo, inicia o servidor
    start_server()
