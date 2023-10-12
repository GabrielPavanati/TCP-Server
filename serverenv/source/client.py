import socket  # Importa o módulo socket para criar e gerenciar conexões de rede

def start_client():
    host = 'localhost'  # Endereço do host onde o servidor está rodando
    port = 5000         # Porta onde o servidor está escutando

    # Cria um novo socket usando o protocolo TCP (SOCK_STREAM)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta-se ao servidor no host e porta especificados
    client_socket.connect((host, port))

    while True:  # Loop principal do cliente
        # Mostra o menu de opções
        menu = """\n
        1 - Encerrar conexão\n
        2 - Mostrar banco de dados\n
        3 - Mostrar gráfico\n"""

        print(menu)
        opcao = input("Selecione uma opção: ")

        # Se a mensagem for 'tchau', recebe a mensagem de encerramento do servidor, fecha a conexão e termina o cliente
        if opcao == '1':
            client_socket.close()
            break  # Quebra o loop, encerrando o cliente

if __name__ == "__main__":  # Verifica se este script é o principal e, em caso afirmativo, inicia o cliente
    start_client()

