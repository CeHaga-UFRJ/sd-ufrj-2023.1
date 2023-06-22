from Types import Content, UserId, Topic, FnNotify

class User():
    def __init__(self, id: UserId, callback: FnNotify):
        self.id = id
        self.callback = callback
        self.topics = []

    def __eq__(self, other):
        return self.id == other.id
    
    def subscribe_to(self, topic: Topic):
        self.topics.append(topic)

    def notify(self, content: Content):
        listContent = [content]
        self.callback(listContent)

    def notifyAll(self, contents: list[Content]):
        self.callback(contents)