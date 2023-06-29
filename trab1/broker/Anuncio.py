from Types import Content

class Anuncio:
    id = 1

    def __init__(self, userId, topic, data):
        self.content = Content(author=userId, topic=topic, data=data)
        self.id = Anuncio.id
        Anuncio.id += 1