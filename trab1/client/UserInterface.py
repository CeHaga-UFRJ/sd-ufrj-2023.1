import sys
sys.path.append('../')

import rpyc
from Types import Content
from Publisher import Publisher
from Subscriber import Subscriber


class UserInterface:
    def __init__(self):
        self.messages = []
        self.menuPrinted = False

    def login(self, userId):
        self.conn = rpyc.connect("localhost", 18861)
        self.bgsrv = rpyc.BgServingThread(self.conn)
        
        hasLogin = self.conn.root.login(userId, self.callback)

        if not hasLogin:
            self.conn.close()
            self.bgsrv.stop()
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
        contentListSize = len(content_list)
        notification = f"Você possui {contentListSize} novos anúncios" if contentListSize > 1 else "Você possui 1 novo anúncio"
        print(notification)
        print()
        for content in content_list:
            self.messages.insert(0,[content, False])
        if not self.menuPrinted:
            return
        print_menu_options()

    def read_message(self, messageId):
        self.messages[messageId][1] = True
        return self.messages[messageId][0]
    
    def list_topics(self):
        return self.conn.root.list_topics()


def login_interface(client):
    while True:
        userId = input("Digite seu nome de usuário: ")
        print()
        hasLogin = client.login(userId)

        if (hasLogin):
            print("Login realizado com sucesso")
            return

        print("Erro: Usuário já está logado")


def menu_interface(client):
    client.menuPrinted = True
    while True:
        print_menu_options()
        option = input()
        print()

        if option == "1":
            list_messages_interface(client)
        elif option == "2":
            list_topics_interface(client)
        elif option == "3":
            publish_interface(client)
        elif option == "4":
            subscribe_interface(client)
        elif option == "5":
            unsubscribe_interface(client)
        elif option == "6":
            return
        else:
            print("Opção inválida")

def print_menu_options():
    print("1 - Listar anúncios")
    print("2 - Listar tópicos")
    print("3 - Publicar um anúncio")
    print("4 - Inscrever em um tópico")
    print("5 - Desinscrever de um tópico")
    print("6 - Sair")
    print("Digite a opção desejada: ", end="")
    sys.stdout.flush()

def list_messages_interface(client):
    print("Anúncios:")
    i = 1
    white = "\033[0m"
    red =  "\033[1;31m"
    for message, isRead in client.messages:
        color = white if isRead else red
        data = message.data if len(
            message.data) < 10 else (message.data[:7] + "...")
        print(f'{color}{i}. {message.author}: {message.topic} - "{data}"')
        i += 1
    print(white)

    while True:
        option = input(
            "Digite o número do anúncio para ler (Ou 'q' para sair): ")
        print()
        if (option == "q"):
            return

        if option.isnumeric() and (int(option) <= len(client.messages) and int(option) >= 1):
            break
        
        print("Opção inválida")

    message = client.read_message(int(option) - 1)
    print(f'{message.author}: {message.topic}\n{message.data}')

def list_topics_interface(client):
    print("Tópicos:")
    i = 1

    topics = client.list_topics()

    for topic in topics:
        print(f'{i}. {topic}')
        i += 1
    print()

    return topics


def publish_interface(client):
    topics = list_topics_interface(client)
    
    while True:
        topicId = input("Digite o número do tópico (Ou 'q' para sair): ")
        print()
        if (topicId == "q"):
            return

        if topicId.isnumeric() and (int(topicId) <= len(topics) and int(topicId) >= 1):
            break

        print("Opção inválida")

    data = input("Digite o conteúdo do anúncio: ")
    topic = topics[int(topicId) - 1]
    print()
    client.publish(topic, data)


def subscribe_interface(client):
    
    topics = list_topics_interface(client)

    while True:
        topicId = input("Digite o número do tópico que deseja se inscrever(Ou 'q' para sair): ")
        print()
        if (topicId == "q"):
            return

        if topicId.isnumeric() and (int(topicId) <= len(topics) and int(topicId) >= 1):
            break

        print("Opção inválida")
    
    topic = topics[int(topicId) - 1]

    client.subscribe_to(topic)


def unsubscribe_interface(client):
    topics = list_topics_interface(client)

    while True:
        topicId = input("Digite o número do tópico que deseja se desinscrever (Ou 'q' para sair): ")
        print()
        if (topicId == "q"):
            return

        if topicId.isnumeric() and (int(topicId) <= len(topics) and int(topicId) >= 1):
            break

        print("Opção inválida")
    
    topic = topics[int(topicId) - 1]
    client.unsubscribe_to(topic)


if __name__ == "__main__":
    client = UserInterface()
    login_interface(client)
    menu_interface(client)
