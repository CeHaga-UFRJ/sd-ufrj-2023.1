import sys
import threading
import select
import rpyc
from rpyc.utils.server import ThreadedServer
from dictionary import Dictionary


class Application(rpyc.Service):
    def __init__(self):
        self.data = Dictionary()
        self.lock = threading.Lock()
        self.help = '\nComandos disponíveis:\n' \
                    'fim (f) - encerra o servidor\n' \
                    'deletar (d) - deleta uma palavra do dicionário\n' \
                    'ajuda (h) - mostra os comandos disponíveis\n'
        self.active_conn = 0

    def on_connect(self, conn):
        print('Nova conexão.')
        self.active_conn += 1

    def on_disconnect(self, conn):
        print('Conexão fechada')
        self.active_conn -= 1

    def exposed_get_translation(self, key):
        return self.translate(key)

    def exposed_add_word(self, key, value):
        return self.add_word(key, value)

    def exposed_delete_word(self, key):
        self.delete_word(key)

    def exposed_save_data(self):
        self.save_data()

    def close_server(self):
        if(self.active_conn != 0): return False
        self.save_data()
        return True

    def add_word(self, key, value):
        self.lock.acquire()
        new = self.data.add(key, value)
        self.lock.release()
        if (new):
            return 'ADD-NEW'
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

srv = None 
app = None

def start_server():
    global srv, app
    print("Servidor começando")
    app = Application()
    srv = ThreadedServer(app, port=5000)
    srv.start()

def close_server():
    if(app.close_server()):
        print("Servidor encerrando")
        srv.close()
        return True
    print("Ainda há conexões ativas")
    return False

def main():
    thread = threading.Thread(target=start_server)
    thread.start()

    while(True):
        cmd = input('Digite um comando: ')
        if cmd=='fim' or cmd=='f':
            if(close_server()): break
        elif cmd=='ajuda' or cmd=='h':
            print(app.help)
        elif cmd=='deletar' or cmd=='d':
            key = input('Digite a palavra a ser deletada: ')
            app.delete_word(key)
        else:
            print('Comando inválido')

    thread.join()
    print('Servidor encerrado')
    

if(__name__ == '__main__'):
    main()