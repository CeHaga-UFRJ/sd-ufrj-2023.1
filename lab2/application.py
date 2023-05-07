import socket
import select
import sys
import pickle
import threading
from dictionary import Dictionary


class Application:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.inputs = [sys.stdin]
        self.connections = {}
        self.data = Dictionary()
        self.lock = threading.Lock()
        self.open_server()
        self.help = '\nComandos disponíveis:\n' \
                    'fim (f) - encerra o servidor\n' \
                    'deletar (d) - deleta uma palavra do dicionário\n' \
                    'ajuda (h) - mostra os comandos disponíveis\n'
    
    def open_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.sock.setblocking(False)
        self.inputs.append(self.sock)
        print('Servidor rodando na porta ', self.port)

    def accept_connection(self):
        conn, addr = self.sock.accept()
        print('Nova conexão de ', addr)
        self.connections[conn.fileno()] = addr

        return conn, addr

    def close_connection(self, conn):
        print('Conexão fechada de ', self.connections[conn.fileno()])
        del self.connections[conn.fileno()]
        conn.close()

    def respond_connections(self, conn, data):
        while True:
            data = conn.recv(1024)
            if not data:
                self.close_connection(conn)
                return
            cmds = data.decode('utf-8').split('\n')
            if(cmds[0] == 'GET'):
                key = cmds[1]
                translation = self.translate(key)
                data_send = pickle.dumps(translation)
                conn.send(data_send)
            elif(cmds[0] == 'ADD'):
                key = cmds[1]
                value = cmds[2]
                conn.send(self.add_word(key, value).encode('utf-8'))

    def run(self):
        threads = []
        print('Aguardando conexões...')
        while True:
            read, _, _ = select.select(self.inputs, [], [])
            for s in read:
                if s is self.sock:
                    conn, addr = self.accept_connection()

                    t = threading.Thread(target=self.respond_connections, args=(conn, addr))
                    t.start()
                    threads.append(t)
                elif s is sys.stdin:
                    cmd = input()
                    if(cmd == 'fim' or cmd == 'f'):
                        print('Fechando servidor...')
                        print('Esperando processos finalizarem...')
                        for t in threads:
                            t.join()
                        print('Processos finalizados!')
                        print('Salvando dados...')
                        self.save_data()
                        print('Finalizando...')
                        self.sock.close()
                        sys.exit()
                    elif(cmd == 'ajuda' or cmd == 'h'):
                        print(self.help)
                    elif(cmd == 'deletar' or cmd == 'd'):
                        key = input('Digite a palavra: ')
                        self.delete_word(key)
                        print('Palavra deletada com sucesso!')
                    else:
                        print('Entre com um comando válido, ou digite ajuda para ver os comandos disponíveis')

    def add_word(self, key, value):
        self.lock.acquire()
        new = self.data.add(key, value)
        self.lock.release()
        if(new):
            return 'ADD-NEW'
        else:
            return 'ADD-OLD'

    def delete_word(self, key):
        self.lock.acquire()
        self.data.delete(key)
        self.lock.release()

    def save_data(self):
        self.lock.acquire()
        self.data.save()
        self.lock.release()

    def translate(self, key):
        self.lock.acquire()
        translation = self.data.translate(key)
        self.lock.release()
        return translation
