# RASCUNHO


class Subscriber:
    def __init__(self, userId, conn):
        self.userId = userId
        self.conn = conn

    def subscribe_to(self, topic, callback):
        return self.conn.root.subscribe_to(self.userId, topic, callback)

    def unsubscribe_to(self, topic):
        return self.conn.root.unsubscribe_to(self.userId, topic)
