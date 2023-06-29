from Types import Content, Topic
from Anuncio import Anuncio

class TopicClass():
    def __init__(self, name: Topic):
        self.name = name
        self.subscribers = []
        self.anuncios = []

    def __eq__(self, other):
        return type(other) is type(self) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def add_subscriber(self, user):
        user.subscribe_to(self)
        self.subscribers.append(user)

    def remove_subscriber(self, user):
        user.unsubscribe_to(self)
        self.subscribers.remove(user)

    def add_anuncio(self, anuncio: Anuncio):
        self.anuncios.append(anuncio)

    def get_subscribers(self):
        subscribers = []
        for subscriber in self.subscribers:
            subscribers.append(subscriber.id)
        return subscribers

        