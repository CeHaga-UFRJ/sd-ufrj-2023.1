from Types import Content, UserId, FnNotify
from Anuncio import Anuncio


class User():
    def __init__(self, id: UserId, callback: FnNotify):
        self.id = id
        self.callback = callback
        self.topics = []
        self.last_notification = {}
        self.logged = True


    def __eq__(self, other):
        return self.id == other.id
    
    def subscribe_to(self, topic):
        self.topics.append(topic)

    def unsubscribe_to(self, topic):
        self.topics.remove(topic)

    def notify(self, anuncio: Anuncio):
        if not self.logged: return
        
        self.last_notification[anuncio.content.topic] = anuncio.id

        listContent = [anuncio.content]
        self.callback(listContent)

        print("Usuario notificado: ", self.id)

    def notifyAll(self, anuncios: list[Anuncio]):
        contents = []

        for anuncio in anuncios:
            if anuncio.content.topic not in self.last_notification:
                self.last_notification[anuncio.content.topic] = anuncio.id
                
            self.last_notification[anuncio.content.topic] = max(anuncio.id, self.last_notification[anuncio.content.topic])
            contents.append(anuncio.content)

        print("Usuario notificado: ", self.id)
        print("Anuncios: ", contents)
        print()
        self.callback(contents)

    def logout(self):
        self.logged = False

    def login(self):
        self.logged = True