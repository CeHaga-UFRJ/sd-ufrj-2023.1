from threading import Thread

from Types import Content, UserId, Topic
from Topic import TopicClass

from User import User

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
    
    def publish(self, content: Content) -> bool:
        topic = content.topic
        if topic in self.topics:

            self.topics[topic].add_anuncio(content)
            print("Publicando anuncio")
            print("Topico: ", topic)
            print("Anuncio publicado: ", content.data)
            print("Anuncios: ", self.topics[topic].anuncios)
            print()
            self.anunciar(content)
            
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
        
    def anunciar(self, conteudo: Content) -> bool:
        subscribers = self.topics[conteudo.topic].subscribers
        print("Anunciando para: ", self.topics[conteudo.topic].get_subscribers())

        for subscriber in subscribers:
            t = Thread(target=subscriber.notify, args=(conteudo,))
            t.start()
        print()    
        
        return True
    

    def list_topics(self) -> list[Topic]:
        return list(self.topics.keys())
    
    def notify_all(self, user: User) -> bool:
        contents = []
        for topic in user.topics:
            for anuncio in topic.anuncios:
                contents.append(anuncio)
        if len(contents) > 0:
            user.notifyAll(contents)
