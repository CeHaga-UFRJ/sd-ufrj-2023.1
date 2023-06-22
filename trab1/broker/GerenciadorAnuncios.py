from Types import Content, UserId, Topic
from Topic import TopicClass

from User import User

class GerenciadorAnuncios(): 
    def __init__(self):
        self.topicos = {}

    def create_topic(self, topicname: str) -> Topic:
        topic = TopicClass(topicname)

        if topic not in self.topicos:
            self.topicos[topicname] = topic

        return topicname
    
    def publish(self, content: Content) -> bool:
        topic = content.topic
        if topic in self.topicos:

            self.topicos[topic].add_anuncio(content)
            self.anunciar(content)
            return True
        else:
            return False
        
    def subscribe_to(self, user: User, topic: Topic) -> bool:
        if topic in self.topicos:
            self.topicos[topic].add_subscriber(user)
            return True
        else:
            return False
        
    def anunciar(self, conteudo: Content) -> bool:
        subscribers = self.topicos[conteudo.topic].subscribers

        for subscriber in subscribers:
            subscriber.notify(conteudo)
        
        return True
    

    def list_topics(self) -> list[Topic]:
        return self.topicos.keys()
    
    def notify_all(self, user: User) -> bool:
        contents = []
        for topic in user.topics:
            for anuncio in topic.anuncios:
                contents.append(anuncio)
        if len(contents) > 0:
            user.notifyAll(contents)