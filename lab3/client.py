from client_side import ClientSide

print('Boas vindas ao cliente!')
client = ClientSide('localhost', 5000)
client.run()