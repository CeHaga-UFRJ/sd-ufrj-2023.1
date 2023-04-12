import socket

HOST = 'localhost'
PORTA = 5000

sock = socket.socket()
sock.connect((HOST, PORTA))

while True:
    msg = input()
    if msg == "fim":
        break
    sock.send(bytes(msg,  encoding='utf-8'))
    msg = sock.recv(1024)
    print('Recebido: ' + str(msg,  encoding='utf-8'))

sock.close()
