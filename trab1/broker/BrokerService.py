# RASCUNHO

from __future__ import annotations

from typing import Callable, TypeAlias

import rpyc
from Types import Content, UserId, Topic


FnNotify: TypeAlias = Callable[[list[Content]], None]


class BrokerService(rpyc.Service):
    def __init__(self):
        self.topics = {}
        self.subscribers = {}

    def create_topic(self, id: UserId, topicname: str) -> Topic:
        if id == "admin":
            topic = Topic(topicname)
            self.topics[topic] = []
            return topic
        else:
            return None

    def exposed_login(self, id: UserId) -> bool:
        if id not in self.subscribers:
            self.subscribers[id] = []
        return True

    def exposed_list_topics(self) -> list[Topic]:
        return list(self.topics.keys())

    def exposed_publish(self, id: UserId, topic: Topic, data: str) -> bool:
        if topic in self.topics:
            content = Content(id, topic, data)
            self.topics[topic].append(content)
            self.notify_subscribers(topic)
            return True
        else:
            return False

    def exposed_subscribe_to(self, id: UserId, topic: Topic, callback: FnNotify) -> bool:
        if topic in self.topics and id in self.subscribers:
            self.subscribers[id].append((topic, callback))
            self.send_missed_messages(id, topic, callback)
            return True
        else:
            return False

    def exposed_unsubscribe_to(self, id: UserId, topic: Topic) -> bool:
        if id in self.subscribers:
            self.subscribers[id] = [
                (t, cb) for t, cb in self.subscribers[id] if t != topic]
            return True
        else:
            return False

    def notify_subscribers(self, topic: Topic) -> None:
        if topic in self.topics:
            content_list = self.topics[topic]
            for subscriber in self.subscribers.values():
                for sub_topic, callback in subscriber:
                    if sub_topic == topic:
                        callback(content_list)

    def send_missed_messages(self, id: UserId, topic: Topic, callback: FnNotify) -> None:
        if topic in self.topics:
            content_list = self.topics[topic]
            callback(content_list)


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(BrokerService, port=18861)
    server.start()
