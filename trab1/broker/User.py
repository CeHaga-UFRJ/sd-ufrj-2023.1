from Types import Content, UserId, Topic

class User():
    def __init__(self, id: UserId):
        self.id = id
        self.callback = {}

    def __eq__(self, other):
        return self.id == other.id
    
    def set_callback(self, Topic, callback):
        self.callback[Topic] = callback

    def notify(self, content: Content):
        listContent = [content]
        self.callback[content.topic](listContent)

    def notifyAll(self, content: Content):
        pass