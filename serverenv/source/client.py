import socket  # Importa o módulo socket para criar e gerenciar conexões de rede

def start_client():
    host = 'localhost'  # Endereço do host onde o servidor está rodando
    port = 5000         # Porta onde o servidor está escutando

    # Cria um novo socket usando o protocolo TCP (SOCK_STREAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta-se ao servidor no host e porta especificados
    client_socket.connect((host, port))

    while True:  # Loop principal do cliente
        # Solicita ao usuário que digite uma mensagem
        message = input("Digite uma mensagem (ou 'tchau' para sair): ")

        # Envia a mensagem ao servidor
        client_socket.sendall(message.encode())

        # Se a mensagem for 'tchau', recebe a mensagem de encerramento do servidor, fecha a conexão e termina o cliente
        if message.lower() == 'tchau':
            data = client_socket.recv(1024)
            print(data.decode())
            client_socket.close()
            break  # Quebra o loop, encerrando o cliente

if __name__ == "__main__":  # Verifica se este script é o principal e, em caso afirmativo, inicia o cliente
    start_client()

