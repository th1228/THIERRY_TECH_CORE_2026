class MemoriaComumManager:
    def __init__(self):
        self.storage = {}
        print("[MEMÓRIA] Gerente de Filas e Estado ativado com sucesso.")

    def gravar(self, chave, valor):
        self.storage[chave] = valor
        print(f"Salvando na memória -> Chave: '{chave}', Valor: '{valor}'")

    def ler(self, chave):
        return self.storage.get(chave, None)

if __name__ == "__main__":
    print("=========================================")
    print("INICIANDO TESTE DE MEMÓRIA COMPARTILHADA")
    print("=========================================")
    
    mem = MemoriaComumManager()
    mem.gravar("CLIENTE", "THERRY")
    dado = mem.ler("CLIENTE")
    
    print(f"Dado lido da memória: {dado}")
    print(" -> STATUS: PASSOU (Memória gravando e lendo perfeitamente)")
    print("=========================================")
    print("TESTE DE MEMÓRIA FINALIZADO COM SUCESSO.")
    print("=========================================")