# RASCUNHO

import rpyc
from Publisher import Publisher
from Subscriber import Subscriber


class UserInterface:
    def __init__(self):
        self.conn = rpyc.connect("localhost", 18861)
        self.bgsrv = rpyc.BgServingThread(self.conn)
        self.messages = []

    def login(self, userId):
        hasLogin = self.conn.root.login(userId, self.callback)
        if not hasLogin:
            return False

        self.userId = userId
        self.publisher = Publisher(self.userId, self.conn)
        self.subscriber = Subscriber(self.userId, self.conn)

        return True

    def publish(self, topic, data):
        self.publisher.publish(topic, data)

    def subscribe_to(self, topic):
        self.subscriber.subscribe_to(topic)

    def unsubscribe_to(self, topic):
        self.subscriber.unsubscribe_to(topic)

    def callback(self, content_list):
        print("Callback chamado")
        print(content_list)

    def read_message(self, messageId):
        self.messages[messageId][1] = True
        return self.messages[messageId][0]


def login_interface(client):
    while True:
        userId = input("Digite seu nome de usuário: ")
        hasLogin = client.login(userId)

        if (hasLogin):
            print("Login realizado com sucesso")
            return

        print("Erro: Usuário já está logado")


def menu_interface(client):
    while True:
        print("1 - Listar anúncios")
        print("2 - Publicar um anúncio")
        print("3 - Inscrever em um tópico")
        print("4 - Desinscrever de um tópico")
        print("5 - Sair")

        option = input("Digite a opção desejada: ")

        if option == "1":
            list_messages_interface(client)
        elif option == "2":
            publish_interface(client)
        elif option == "3":
            subscribe_interface(client)
        elif option == "4":
            unsubscribe_interface(client)
        elif option == "5":
            return
        else:
            print("Opção inválida")


def list_messages_interface(client):
    print("Anúncios:")
    i = 1
    for message, isRead in client.messages:
        color = "\033[0m" if isRead else "\033[1;31m"
        data = message.data if len(
            message.data) < 7 else message.data[:10] + "..."
        print(f'{color}{i}. {message.author}: {message.topic} - "{data}"')
        i += 1

    while True:
        option = input(
            "Digite o número do anúncio para ler (Ou 'q' para sair): ")
        if (option == "q"):
            return

        if (int(option) > len(client.messages) or int(option) < 1):
            print("Opção inválida")
            continue

        message = client.read_message(int(option) - 1)
        print(f'{message.author}: {message.topic}\n{message.data}')


def publish_interface(client):
    topic = input("Digite o nome do tópico: ")
    data = input("Digite o conteúdo do anúncio: ")
    client.publish(topic, data)


def subscribe_interface(client):
    topic = input("Digite o nome do tópico a se inscrever: ")
    client.subscribe_to(topic)


def unsubscribe_interface(client):
    topic = input("Digite o nome do tópico a se desinscrever: ")
    client.unsubscribe_to(topic)


if __name__ == "__main__":
    client = UserInterface()
    login_interface(client)
    menu_interface(client)
