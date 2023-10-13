# 🌡️ Servidor e Cliente TCP em Python

Este é um projeto de cliente e servidor TCP em Python que fornece dados de temperatura entre 20 e 30 graus Celsius. O cliente captura esses dados e os salva em um banco de dados SQLite.

## 📋 Estrutura do Repositório

O repositório está organizado da seguinte maneira:

- `serverenv/`: Ambiente virtual Python para o servidor.
- `serverenv/source/`: Contém os arquivos Python para o cliente e servidor.

## 🚀 Configuração do Ambiente

Para configurar o ambiente virtual para o servidor, siga os passos abaixo:

1. Navegue até o diretório `serverenv/`.
2. Ative o ambiente virtual:

   ```bash
   .\Scripts\activate  # No Windows

## 🏃 Executando o Servidor

Para iniciar o servidor, siga os passos abaixo:

1. Navegue até a pasta `serverenv/source/`.
   
   ```bash
   cd serverenv/source/

2. Execute o servidor:
   
      ```bash
     python server.py

O servidor estará pronto para fornecer dados de temperatura.

## 📡 Executando o Cliente

O cliente pode ser executado com o seguinte comando na pasta `source/`:

```bash
python client.py
```

O cliente capturará os dados de temperatura do servidor e os salvará em um banco de dados SQLite.
