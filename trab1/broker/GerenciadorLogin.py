from Types import UserId


class GerenciadorLogin():
    def __init__(self):
        self.usuarios_logados = []

    def login(self, id: UserId) -> bool:
        if id not in self.usuarios_logados:
            self.usuarios_logados.append(id)
            return True
        else:
            return False

    def logout(self, id: UserId) -> bool:
        if id in self.usuarios_logados:
            self.usuarios_logados.remove(id)
            return True
        else:
            return False

    def list_users(self) -> list[UserId]:
        return self.usuarios_logados