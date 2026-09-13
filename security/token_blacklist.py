class TokenBlacklist:
    def __init__(self):
        self.blacklist = set()

    def bloquear(self, token):
        self.blacklist.add(token)

    def esta_bloqueado(self, token):
        return token in self.blacklist