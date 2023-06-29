from Types import UserId, FnNotify
from User import User


class GerenciadorLogin():
    def __init__(self):
        self.usuarios_logados = []

    def login(self, user: User) -> bool:
        if user not in self.usuarios_logados:
            user.login()
            self.usuarios_logados.append(user)
            print(f"Usuário {user.id} logado com sucesso!")
            print ("Usuários logados:")
            print (self.get_users())
            print()
            return True
        else:
            return False

    def logout(self, user: User) -> bool:
        if user in self.usuarios_logados:
            user.logout()
            self.usuarios_logados.remove(user)
            print(f"Usuário {user.id} deslogado com sucesso!")
            print ("Usuários logados:")
            print (self.get_users())
            print()
            return True
        else:
            return False

    def list_users(self) -> list[UserId]:
        return self.usuarios_logados
    
    def get_user(self, id: UserId) -> User:
        for user in self.usuarios_logados:
            if user.id == id:
                return user
        return None
    
    def get_users(self) -> list[User]:
        users = []
        for user in self.usuarios_logados:
            users.append(user.id)

        return users
