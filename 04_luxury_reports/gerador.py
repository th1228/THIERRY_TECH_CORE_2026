import datetime
from cryptography.fernet import Fernet

# 1. Defina sua chave única aqui
# Se você tiver uma chave que já usa no sistema, cole-a dentro do b''
KEY = Fernet.generate_key() 
cipher_suite = Fernet(KEY)

def gerar_nova_licenca():
    print("--- GERADOR DE SOBERANIA TTC GLOBAL ---")
    
    # Coleta de dados
    nome = input("Nome do Cliente: ")
    prazo = input("Digite o prazo (6, 12 ou 24): ")
    data_hoje = datetime.date.today().strftime("%Y-%m-%d")
    
    # Formatação do dado (Soberania de dados)
    texto_final = f"{nome}|{prazo}|{data_hoje}"
    
    # Criptografia
    token = cipher_suite.encrypt(texto_final.encode())
    
    # Saída
    print("\n[SUCESSO] Chave de Acesso gerada:")
    print(token.decode())
    print("\n[IMPORTANTE] Guarde esta chave em local seguro.")
    print(f"Chave mestre usada para gerar: {KEY.decode()}")

if __name__ == "__main__":
    gerar_nova_licenca()