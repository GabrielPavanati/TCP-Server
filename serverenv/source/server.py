import socket  # Importa o módulo socket para criar e gerenciar conexões de rede

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

    while True:  # Loop principal do servidor
        # Aceita uma nova conexão de cliente
        conn, addr = server_socket.accept()

        print(f"Conexão estabelecida com {addr}")

        while True:  # Loop de comunicação com o cliente
            # Recebe dados do cliente (bloqueia até que os dados sejam recebidos)
            data = conn.recv(1024)

            # Se não receber dados, quebra o loop (conexão fechada pelo cliente)
            if not data:
                break

            # Decodifica os dados recebidos de bytes para string
            message = data.decode()

            print(f"Mensagem recebida: {message}")

            # Se a mensagem for 'tchau', envia uma mensagem de encerramento, fecha a conexão e termina o servidor
            if message.lower() == 'tchau':
                conn.sendall("Servidor encerrado pelo cliente".encode())
                conn.close()
                print("Conexão encerrada")
                return  # Retorna da função, encerrando o servidor

        # Fecha a conexão com o cliente
        conn.close()

if __name__ == "__main__":  # Verifica se este script é o principal e, em caso afirmativo, inicia o servidor
    start_server()

