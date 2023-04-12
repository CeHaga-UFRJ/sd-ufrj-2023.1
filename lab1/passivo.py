import socket

# Dados de conexão
HOST = ''
PORTA = 5000

# Cria o socket
sock = socket.socket()

# Associa o socket a porta
sock.bind((HOST, PORTA))

# Aguarda conexões
sock.listen(5)
print("Pronto para receber conexões...")

# Aceita a conexão
novoSock, endereco = sock.accept()
print('Conectado com: ', endereco)

while True:
    # Recebe a mensagem do ativo
    msg = novoSock.recv(1024)

    # Verifica se a conexão foi encerrada
    if not msg:
        break

    # Envia a mensagem de volta
    # Não é necessário converter para bytes pois já veio no formato
    print('Mensagem recebida')
    novoSock.send(msg)

# Fecha os sockets
novoSock.close()
sock.close()
