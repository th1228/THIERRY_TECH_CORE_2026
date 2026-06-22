import sys
import os

# Adiciona o diretório raiz ao path. Isso força o Python a reconhecer a estrutura de pastas.
# Usamos o caminho absoluto para evitar qualquer erro de localização.
diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
if diretorio_raiz not in sys.path:
    sys.path.append(diretorio_raiz)

# Importações explícitas dos seus módulos na pasta 'core'
# Usamos o prefixo 'core.' para deixar claro que os arquivos estão lá dentro
from core import seguranca
from core import motor_dados
from core import atelie

def main():
    print("-" * 35)
    print("INICIANDO SISTEMA TTC CORE 2026")
    print("-" * 35)
    
    try:
        # 1. Validação de Segurança
        if seguranca.verificar_seguranca():
            print("[MAIN] Segurança validada com sucesso.")
        
        # 2. Inicialização dos Motores
        print("[MAIN] Carregando motor de dados...")
        motor_dados.inicializar_sistema()
        
        # 3. Inicialização do Ateliê
        print("[MAIN] Inicializando módulos do ateliê...")
        atelie.iniciar()
        
        print("\n[MAIN] Sistema operando em nível total.")
        
    except PermissionError as e:
        print(f"\n[ERRO DE BLOQUEIO]: {e}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")
        # Isso ajuda a ver o erro exato se acontecer algo novo
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()