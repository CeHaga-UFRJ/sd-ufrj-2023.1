class Publisher:
    def __init__(self, userId, conn):
        self.userId = userId
        self.conn = conn

    def publish(self, topic, data):
        return self.conn.root.publish(self.userId, topic, data)
