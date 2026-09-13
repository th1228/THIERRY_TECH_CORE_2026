import hashlib

class DataAnonymizer:
    @staticmethod
    def anonimizar(dado):
        """Transforma um dado sensível em um hash irreversível."""
        return hashlib.sha256(str(dado).encode()).hexdigest()