import rpyc


class ClientSide:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = rpyc.connect(self.host, self.port)
        self.help = '\nComandos disponíveis:\n' \
                    'fim (f) - encerra o cliente\n' \
                    'consultar (c) - consulta uma tradução\n' \
                    'adicionar (a) - adiciona uma tradução\n' \
                    'ajuda (h) - mostra os comandos disponíveis\n'

    def run(self):
        while True:
            cmd = input('Digite um comando: ')
            if cmd == 'fim' or cmd == 'f':
                break
            elif cmd == 'ajuda' or cmd == 'h':
                print(self.help)
            elif cmd == 'consultar' or cmd == 'c':
                key = input('Digite a palavra a ser consultada: ')
                translation = self.conn.root.get_translation(key)
                print('Traduções:', translation)
            elif cmd == 'adicionar' or cmd == 'a':
                key = input('Digite a palavra a ser adicionada: ')
                value = input('Digite a tradução da palavra: ')
                response = self.conn.root.add_word(key, value)
                if response == 'ADD-NEW':
                    print('Palavra adicionada com sucesso!')
                elif response == 'ADD-OLD':
                    print('Palavra já existente no dicionário!')
            else:
                print(
                    'Entre com um comando válido, ou digite ajuda para ver os comandos disponíveis')
        self.conn.close()
        print('Cliente encerrado!')
