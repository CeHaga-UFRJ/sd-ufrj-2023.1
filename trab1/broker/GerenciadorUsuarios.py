from Types import UserId, FnNotify
from User import User

class GerenciadorUsuarios():
    def __init__(self):
        self.all_users = []

    def add_user(self, user: User) -> bool:
        if user not in self.all_users:
            self.all_users.append(user)
            return True
        else:
            return False
        
    def get_user(self, id: UserId, callback) -> User:
        for user in self.all_users:
            if user.id == id:
                user.callback = callback
                return user
            
        user = User(id, callback)
        self.all_users.append(user)
        return user
    


    