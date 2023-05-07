import socket
import pickle

class ClientSide:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.help = '\nComandos disponíveis:\n' \
                    'fim (f) - encerra o cliente\n' \
                    'consultar (c) - consulta uma tradução\n' \
                    'adicionar (a) - adiciona uma tradução\n' \
                    'ajuda (h) - mostra os comandos disponíveis\n'

    def send_receive(self, data):
        self.sock.send(data)
        data = self.sock.recv(1024)
        return data

    def run(self):
        while True:
            cmd = input('Digite um comando: ')
            if cmd == 'fim' or cmd == 'f':
                break
            elif cmd == 'ajuda' or cmd == 'h':
                print(self.help)
            elif cmd == 'consultar' or cmd == 'c':
                key = input('Digite a palavra a ser consultada: ')
                data = ('GET\n' + key).encode('utf-8')
                translation_raw = self.send_receive(data)
                translation = pickle.loads(translation_raw)
                print('Traduções: ', end='')
                print(translation)
            elif cmd == 'adicionar' or cmd == 'a':
                key = input('Digite a palavra a ser adicionada: ')
                value = input('Digite a tradução da palavra: ')
                data = ('ADD\n' + key + '\n' + value).encode('utf-8')
                response = self.send_receive(data).decode('utf-8')
                if(response == 'ADD-NEW'):
                    print('Palavra adicionada com sucesso!')
                elif(response == 'ADD-OLD'):
                    print('Palavra já existente no dicionário!')
            else:
                print('Entre com um comando válido, ou digite ajuda para ver os comandos disponíveis')
        print('Cliente encerrado!')