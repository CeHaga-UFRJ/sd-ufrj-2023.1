# RASCUNHO

import rpyc
import Publisher
import Subscriber


class UserInterface:
    def __init__(self):
        self.conn = rpyc.connect("localhost", 18861)

    def login(self, userId):
        # Verifica se userId é válido (Chamar função login do BrokerService)
        self.userId = userId
        self.publisher = Publisher(self.userId, self.conn)
        self.subscriber = Subscriber(self.userId, self.conn)


if __name__ == "__main__":
    client = UserInterface()
    client.run_publisher()
    client.run_subscriber()
