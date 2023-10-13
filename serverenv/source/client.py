import socket  # Importa o módulo socket para criar e gerenciar conexões de rede
import threading

# Função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
        except Exception as e:
            print("Erro ao receber dados do servidor:", str(e))
            break

# Função para mostrar um menu e selecionar opções
def send_options(client_socket):
    while True:
        # Mostra o menu e pede para o usuário inserir uma opção
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
            

def start_client():
    host = 'localhost'  # Endereço do host onde o servidor está rodando
    port = 5000         # Porta onde o servidor está escutando

    # Cria um novo socket usando o protocolo TCP (SOCK_STREAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta-se ao servidor no host e porta especificados
    client_socket.connect((host, port))

    # Crie threads para receber e enviar mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_options, args=(client_socket,))

    # Inicie as threads
    receive_thread.start()
    send_thread.start()

    # Aguarde o término das threads
    receive_thread.join()
    send_thread.join()

if __name__ == "__main__":  # Verifica se este script é o principal e, em caso afirmativo, inicia o cliente
    start_client()
