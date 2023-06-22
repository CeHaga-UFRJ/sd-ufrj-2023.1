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

        print("Topico criado: ", topicname)
        print("Topicos: ", self.topicos)
        print()

        return topicname
    
    def publish(self, content: Content) -> bool:
        topic = content.topic
        if topic in self.topicos:

            self.topicos[topic].add_anuncio(content)
            print("Topico: ", topic)
            print("Anuncio publicado: ", content.topic, content.data)
            print("Anuncios: ", self.topicos[topic].anuncios)
            self.anunciar(content)
            
            print()
            return True
        else:
            return False
        
    def subscribe_to(self, user: User, topic: Topic) -> bool:
        if topic in self.topicos:
            self.topicos[topic].add_subscriber(user)
            print("Topico: ", topic)
            print("Usuario inscrito: ", user.id)
            print("Usuarios inscritos: ", self.topicos[topic].subscribers)
            print()
            return True
        else:
            return False
        
    def anunciar(self, conteudo: Content) -> bool:
        subscribers = self.topicos[conteudo.topic].subscribers
        print("Usuarios a serem notificados:", subscribers)
        for subscriber in subscribers:
            print("Usuario a ser notificado: ", subscriber.id)
            subscriber.notify(conteudo)
            print("Usuario notificado: ", subscriber.id)
            print()
        
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