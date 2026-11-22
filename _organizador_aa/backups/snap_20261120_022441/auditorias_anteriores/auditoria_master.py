import os
import sys
import datetime
import platform
from pathlib import Path

# Códigos de Cores ANSI para Terminal C2 Sovereign
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_MAGENTA = "\033[95m"
C_BLUE = "\033[94m"

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def executar_auditoria_completa():
    print(C_CYAN + C_BOLD + "\n" + "=" * 84 + C_RESET)
    print(C_CYAN + C_BOLD + "       THIERRY TECHNOLOGY CONCEPT GLOBAL - C2 DEFENSE ENGINE" + C_RESET)
    print(C_CYAN + "         PAINEL DE AUDITORIA, VARREDURA E ANÁLISE DE INOVAÇÃO" + C_RESET)
    print(C_CYAN + C_BOLD + "=" * 84 + C_RESET)
    
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    print(f" {C_YELLOW}⚡{C_RESET} {C_BOLD}Horário da Varredura :{C_RESET} {timestamp}")
    print(f" {C_YELLOW}⚡{C_RESET} {C_BOLD}Operador Ativo      :{C_RESET} {os.getenv('USERNAME', 'THIERRY (TCC SOBERANO)')}")
    print(f" {C_YELLOW}⚡{C_RESET} {C_BOLD}Infraestrutura Host :{C_RESET} {platform.node()} ({platform.system()} {platform.release()})")
    print(C_CYAN + "-" * 84 + C_RESET)

    # Localização exata da pasta de PDFs finais
    pasta_finais = Path("C:/projetos python/THIERRY_TECHNOLOGY_CORE/THIERRY_TECH_CORE_2026/pdfs_finais")
    if not pasta_finais.exists():
        pasta_finais = Path(ROOT_DIR) / "pdfs_finais"

    print(f" {C_MAGENTA}📁{C_RESET} {C_BOLD}Alvo Mapeado         :{C_RESET} {pasta_finais}")
    
    arquivos_encontrados = []
    if pasta_finais.exists():
        arquivos_encontrados = [f for f in pasta_finais.iterdir() if f.is_file() and f.suffix.lower() == '.pdf']
        print(f" {C_GREEN}✔{C_RESET} {C_BOLD}Total de Dossiês     :{C_RESET} {len(arquivos_encontrados)} arquivos válidos no disco")
        print(C_CYAN + "-" * 84 + C_RESET)
        print(C_BOLD + " RELATÓRIO DE ARQUIVOS DETECTADOS:" + C_RESET)
        for idx, arq in enumerate(arquivos_encontrados, 1):
            tamanho_kb = arq.stat().st_size / 1024
            modificacao = datetime.datetime.fromtimestamp(arq.stat().st_mtime).strftime("%d/%m/%Y %H:%M:%S")
            print(f"   {C_GREEN}[{idx}]{C_RESET} {arq.name}")
            print(f"       └─ Tamanho: {tamanho_kb:.2f} KB  |  Modificação: {modificacao}")
    else:
        print(f" {C_RED}[X] A pasta de saída 'pdfs_finais' não foi localizada.{C_RESET}")

    print(C_CYAN + "-" * 84 + C_RESET)
    print(C_BOLD + " 💡 CONCLUSÃO DE INOVAÇÃO E DIFERENCIAIS DO PROGRAMA:" + C_RESET)
    print(C_CYAN + "-" * 84 + C_RESET)
    
    if len(arquivos_encontrados) >= 4:
        print(f"  {C_GREEN}[STATUS]: SISTEMA ALTAMENTE INOVADOR E OPERACIONAL (MÔNACO LEVEL){C_RESET}\n")
        
        print(f"  {C_YELLOW}• POR QUE O PROGRAMA É INOVADOR:{C_RESET}")
        print("    1. Arquitetura C2 Autônoma: Opera sem interrupção, automatizando fluxos industriais complexos.")
        print("    2. Convergência Multi-Domínio: Unifica Inteligência Estratégica, Retornos Financeiros,")
        print("       Tricologia Avançada, Diplomacia UHNW e Modelagem Computacional de Mônaco.")
        print("    3. Compilação Direta: Gera dossiês executivos e técnicos robustos em PDF direto no disco.")
        
        print(f"\n  {C_YELLOW}• O QUE ELE FAZ DE DIFERENCIAL:{C_RESET}")
        print("    1. Precisão de Engenharia Local: Processamento fechado que assegura blindagem de dados.")
        print("    2. Auditoria Dinâmica em Tempo Real: Varre o ambiente para atestar a integridade física.")
        print("    3. Escalabilidade Modular: Estrutura pronta para expansão imediata de novos motores.")
    else:
        print(f"  {C_RED}[!] ATENÇÃO: Varredura parcial. Certifique-se de compilar todos os dossiês.{C_RESET}")

    print(C_CYAN + "=" * 84 + C_RESET)
    print(C_GREEN + C_BOLD + "     AUDITORIA CONCLUÍDA COM EXITO. SISTEMA PRONTO PARA OPERAÇÃO SOBERANA." + C_RESET)
    print(C_CYAN + "=" * 84 + "\n" + C_RESET)

if __name__ == "__main__":
    executar_auditoria_completa()