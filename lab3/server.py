import select
import sys
from application import Application

app = Application(5000)
print('Boas vindas ao servidor!')

inputs = [sys.stdin, app.server]

while True:
    read, _, _ = select.select(inputs, [], [])
    for s in read:
        if s is app.server:
            app.server._handle_request()
        elif s is sys.stdin:
            cmd = input()
            if (cmd == 'fim' or cmd == 'f'):
                app.close_server()
                sys.exit()
            elif (cmd == 'ajuda' or cmd == 'h'):
                print(app.help)
            elif (cmd == 'deletar' or cmd == 'd'):
                key = input('Digite a palavra: ')
                app.delete_word(key)
                print('Palavra deletada com sucesso!')
            else:
                print(
                    'Entre com um comando válido, ou digite ajuda para ver os comandos disponíveis')
