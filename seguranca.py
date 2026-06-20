import os
from pathlib import Path
from dotenv import load_dotenv

# Como o .env e o seguranca.py estão na mesma pasta (visto na sua foto):
caminho_atual = Path(__file__).resolve().parent
caminho_env = caminho_atual / ".env"

# Carrega as chaves
load_dotenv(dotenv_path=caminho_env, override=True)

def verificar_seguranca():
    usuario = os.getenv("DB_USER")
    nivel = os.getenv("NIVEL_ACESSO")
    
    print("-" * 35)
    if usuario:
        print(f"ACESSO CONFIRMADO: {usuario}")
        print(f"NÍVEL: {nivel}")
        print("SISTEMA TTC CORE ATIVADO")
    else:
        print("ALERTA: Chaves não encontradas!")
        # Se der erro, ele te avisa exatamente onde procurou:
        print(f"O Python buscou em: {caminho_env}")
    print("-" * 35)

if __name__ == "__main__":
    verificar_seguranca()