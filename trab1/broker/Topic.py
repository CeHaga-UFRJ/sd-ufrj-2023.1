from Types import Content, UserId, Topic

class TopicClass():
    def __init__(self, name: Topic):
        self.name = name
        self.subscribers = []
        self.anuncios = []

    def __eq__(self, other):
        return self.name == other.name
    
    def add_subscriber(self, id: UserId):
        self.subscribers.append(id)

    def add_anuncio(self, content: Content):
        self.anuncios.append(content)