from Types import Content, UserId, Topic
import Topic
import User

class GerenciadorAnuncios(): 
    def __init__(self):
        self.topicos = {}

    def create_topic(self, topicname: str) -> Topic:
        topic = Topic(topicname)

        if topic not in self.topicos:
            self.topicos[topicname] = topic

        return topicname
    
    def publish(self, content: Content) -> bool:
        topic = Topic(content.topic)

        if topic in self.topicos:
            self.topicos[topic].add_anuncio(content)
            return True
        else:
            return False
        
    def subscribe_to(self, id: UserId, topic: Topic) -> bool:
        if topic in self.topicos:
            self.topicos[topic].add_subscriber(id)
            return True
        else:
            return False
        
    def anunciar(self, conteudo: Content) -> bool:
        subscribers = self.topicos[Content.topic].subscribers

        for subscriber in subscribers:
            subscriber.notify(conteudo)
        
        return True
    

    def list_topics(self) -> list[Topic]:
        return self.topicos.keys()
        