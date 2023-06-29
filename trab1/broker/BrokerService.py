
from __future__ import annotations

import sys
sys.path.append('../')

import threading
import rpyc

from Types import Content, UserId, Topic, FnNotify
from GerenciadorAnuncios import GerenciadorAnuncios
from GerenciadorLogin import GerenciadorLogin
from User import User


class BrokerService(rpyc.Service):  # type: ignore
    def __init__(self):
        self.gerenciadorLogin = GerenciadorLogin()
        self.gerenciadorAnuncios = GerenciadorAnuncios()
        self.create_topic("", "default")
        self.create_topic("", "teste")
        self.create_topic("", "teste2")
        self.connected = {}
        self.lastConnection = None

    def on_connect(self, conn):
        self.connected[conn] = None
        self.lastConnection = conn
        print(self.connected)

    def on_disconnect(self, conn):
        if conn not in self.connected: return
        
        self.gerenciadorLogin.logout(self.connected[conn])
        self.connected.pop(conn)

    # Não é exposed porque só o "admin" tem acesso
    def create_topic(self, id: UserId, topicname: str) -> Topic:

        return self.gerenciadorAnuncios.create_topic(topicname)

    # Handshake

    def exposed_login(self, id: UserId, callback: FnNotify) -> bool:
        """
        Função responde se `id` conseguiu se logar
        """
        user = User(id, callback)
        success = self.gerenciadorLogin.login(user)
        if success:
            self.connected[self.lastConnection] = user
            self.lastConnection = None
            self.gerenciadorAnuncios.notify_all(user)
        else:
            self.connected.pop(self.lastConnection)
            self.lastConnection = None
        return success

    # Query operations

    def exposed_list_topics(self) -> list[Topic]:
        return self.gerenciadorAnuncios.list_topics()

    # Publisher operations

    def exposed_publish(self, id: UserId, topic: Topic, data: str) -> bool:
        """
        Função responde se Anúncio conseguiu ser publicado
        """
        content = Content(author=id, topic=topic, data=data)
        return self.gerenciadorAnuncios.publish(content)

    # Subscriber operations

    def exposed_subscribe_to(self, id: UserId, topic: Topic) -> bool:
        """
        Função responde se `id` está inscrito no `topic`
        """
        user = self.gerenciadorLogin.get_user(id)

        return self.gerenciadorAnuncios.subscribe_to(user, topic)

    def exposed_unsubscribe_to(self, id: UserId, topic: Topic) -> bool:
        """
        Função responde se `id` não está inscrito no `topic`
        """
        user = self.gerenciadorLogin.get_user(id)

        return self.gerenciadorAnuncios.unsubscribe_to(user, topic)


def iniciaServidor():
    server = rpyc.ThreadedServer(BrokerService(), port=18861)
    server.start()


if __name__ == "__main__":
    print("Iniciando servidor...")
    print("Digite 'criar' para criar um tópico")
    t = threading.Thread(target=iniciaServidor)
    t.start()

    while True:
        comando = input()
        if comando == "criar":
            print("Digite o nome do tópico")
            nome = input()
            BrokerService().create_topic("", nome)
