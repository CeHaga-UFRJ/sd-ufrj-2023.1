from threading import Thread

from Types import Content, UserId, Topic
from Topic import TopicClass

from User import User
from Anuncio import Anuncio

class GerenciadorAnuncios(): 
    def __init__(self):
        self.topics = {}

    def create_topic(self, topicname: str) -> Topic:
        topic = TopicClass(topicname)

        if topic not in self.topics:
            self.topics[topicname] = topic

        print("Topico criado: ", topicname)
        print("Topicos: ", self.list_topics())
        print()

        return topicname
    
    def publish(self, anuncio: Anuncio) -> bool:
        topic = anuncio.content.topic
        if topic in self.topics:
            
            self.topics[topic].add_anuncio(anuncio)
            print("Publicando anuncio")
            print("Topico: ", topic)
            print("Anuncio publicado: ", anuncio.content.data)
            print("Anuncios: ", self.topics[topic].anuncios)
            print()
            self.anunciar(anuncio)
            
            print()
            return True
        else:
            return False
        
    def subscribe_to(self, user: User, topic: Topic) -> bool:
        topic = TopicClass(topic)

        if topic.name in self.topics and topic not in user.topics:
            self.topics[topic.name].add_subscriber(user)
            print("Inscrição em tópico")
            print("Topico: ", topic.name)
            print("Usuario inscrito: ", user.id)
            print("Inscritos: ", self.topics[topic.name].get_subscribers())
            print()
            return True
        else:
            return False
        
    def unsubscribe_to(self, user: User, topic: Topic) -> bool:
        topic = TopicClass(topic)

        if topic.name in self.topics and topic in user.topics:
            self.topics[topic.name].remove_subscriber(user)
            print("Desinscrição em tópico")
            print("Topico: ", topic.name)
            print("Usuario desinscrito: ", user.id)
            print("Inscritos: ", self.topics[topic.name].get_subscribers())
            print()
            return True
        else:
            return False
        
    def anunciar(self, anuncio: Anuncio) -> bool:
        subscribers = self.topics[anuncio.content.topic].subscribers
        print("Anunciando para: ", self.topics[anuncio.content.topic].get_subscribers())

        for subscriber in subscribers:
            subscriber.notify(anuncio)
        print()    
        
        return True
    

    def list_topics(self) -> list[Topic]:
        return list(self.topics.keys())
    
    def notify_all(self, user: User) -> bool:
        contents = []
        for topic in user.topics:
            contents += [anuncio for anuncio in topic.anuncios if topic.name not in user.last_notification or user.last_notification[topic.name] < anuncio.id]

        if len(contents) > 0:
            user.notifyAll(contents)
