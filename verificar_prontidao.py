import os
import sys

# Lista de arquivos essenciais que o ecossistema TTC precisa para estar completo
ARQUIVOS_ESSENCIAIS = [
    "teste_camera.py",
    "testar_seguranca.py",
    "testar_motor.py",
    "testar_memoria.py",
    "teste_orquestracao.py"
]

def verificar_projeto():
    print("================================================================")
    print(" [TTC CORE] AUDITORIA DE PRONTIDÃO PARA EMPACOTAMENTO (ZIP)")
    print("================================================================")
    
    diretorio_atual = os.getcwd()
    print(f" Diretório de Trabalho: {diretorio_atual}\n")
    
    arquivos_faltando = []
    arquivos_encontrados = 0

    print(" Verificando integridade dos módulos principais:")
    for arquivo in ARQUIVOS_ESSENCIAIS:
        caminho_completo = os.path.join(diretorio_atual, arquivo)
        if os.path.exists(caminho_completo):
            print(f"   [✓] {arquivo} -> OK")
            arquivos_encontrados += 1
        else:
            print(f"   [X] {arquivo} -> FALTANDO!")
            arquivos_faltando.append(arquivo)

    print("\n----------------------------------------------------------------")
    print(f" Resumo: {arquivos_encontrados}/{len(ARQUIVOS_ESSENCIAIS)} módulos essenciais localizados.")
    print("----------------------------------------------------------------")

    if len(arquivos_faltando) == 0:
        print(" 👑 VEREDITO: SISTEMA 100% COMPLETO E INTEGRO!")
        print(" 🚀 O seu ecossistema está pronto para ser zipado com segurança absoluta.")
        print("================================================================")
        return True
    else:
        print(" ⚠️  VEREDITO: ATENÇÃO! Faltam alguns arquivos para o fechamento.")
        print(f"     Arquivos pendentes: {arquivos_faltando}")
        print("================================================================")
        return False

if __name__ == "__main__":
    verificar_projeto()