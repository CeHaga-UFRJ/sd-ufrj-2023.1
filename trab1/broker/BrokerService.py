# RASCUNHO

from __future__ import annotations

import rpyc
import sys
sys.path.append('../')

from Types import Content, UserId, Topic, FnNotify
from User import User

from GerenciadorLogin import GerenciadorLogin
from GerenciadorAnuncios import GerenciadorAnuncios



class BrokerService(rpyc.Service): # type: ignore

    def __init__(self):
        self.gerenciadorLogin = GerenciadorLogin()
        self.gerenciadorAnuncios = GerenciadorAnuncios()
        self.create_topic("", "default")
        self.create_topic("", "teste")
        self.create_topic("", "teste2")

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
            self.gerenciadorAnuncios.notify_all(user)
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
        return self.gerenciadorAnuncios.unsubscribe_to(id, topic)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(BrokerService(), port=18861)
    server.start()
