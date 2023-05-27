import sys
import threading
import rpyc
from rpyc.utils.server import ThreadedServer
from dictionary import Dictionary


class Application(rpyc.Service):
    def __init__(self, port):
        self.port = port
        self.server = ThreadedServer(Application, port=self.port)
        self.server.start()
        self.inputs = [sys.stdin]
        self.connections = {}
        self.data = Dictionary()
        self.lock = threading.Lock()
        self.help = '\nComandos disponíveis:\n' \
                    'fim (f) - encerra o servidor\n' \
                    'deletar (d) - deleta uma palavra do dicionário\n' \
                    'ajuda (h) - mostra os comandos disponíveis\n'

    def on_connect(self, conn):
        print('Nova conexão de ', conn.fileno())
        # self.connections[conn.fileno()] = conn

    def close_connection(self, conn):
        print('Conexão fechada de ', self.connections[conn.fileno()])
        # del self.connections[conn.fileno()]
        # conn.close()

    def exposed_get_translation(self, key):
        return self.translate(key)

    def exposed_add_word(self, key, value):
        return self.add_word(key, value)

    def exposed_delete_word(self, key):
        self.delete_word(key)

    def exposed_save_data(self):
        self.save_data()

    def close_server(self):
        self.save_data()
        self.server.close()

    def add_word(self, key, value):
        self.lock.acquire()
        new = self.data.add(key, value)
        self.lock.release()
        if (new):
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
