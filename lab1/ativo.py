import socket

# Dados de conexão
HOST = 'localhost'
PORTA = 5000

# Cria o socket
sock = socket.socket()
sock.connect((HOST, PORTA))

while True:
    # Le a mensagem
    msg = input()

    # Verifica se é para terminar
    if msg == "fim":
        break

    # Envia a mensagem
    sock.send(bytes(msg,  encoding='utf-8'))

    # Recebe a mensagem do passivo
    msg = sock.recv(1024)

    print('Recebido: ' + str(msg,  encoding='utf-8'))

# Fecha o socket
sock.close()
