# RASCUNHO

from __future__ import annotations

from typing import Callable, TypeAlias

import rpyc
from Types import Content, UserId, Topic

import GerenciadorLogin
import GerenciadorAnuncios

FnNotify: TypeAlias = Callable[[list[Content]], None]


class BrokerService(rpyc.Service):
    def __init__(self):
        self.gerenciadorLogin = GerenciadorLogin()
        self.gerenciadorAnuncios = GerenciadorAnuncios()
        self.create_topic("default")
        self.create_topic("teste")
        self.create_topic("teste2")

    def create_topic(self, id: UserId, topicname: str) -> Topic:
        return self.gerenciadorAnuncios.create_topic(topicname)

    def exposed_login(self, id: UserId) -> bool:
        success = self.gerenciadorLogin.login(id)
        if success:
            self.user.notifyAll()
        return success

    def exposed_list_topics(self) -> list[Topic]:
        return self.gerenciadorAnuncios.list_topics()

    def exposed_publish(self, id: UserId, topic: Topic, data: str) -> bool:
        return self.gerenciadorAnuncios.publish(Content(id, topic, data))
        

    def exposed_subscribe_to(self, id: UserId, topic: Topic, callback: FnNotify) -> bool:
        return self.gerenciadorAnuncios.subscribe_to(id, topic, callback)

    def exposed_unsubscribe_to(self, id: UserId, topic: Topic) -> bool:
        pass

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(BrokerService, port=18861)
    server.start()
