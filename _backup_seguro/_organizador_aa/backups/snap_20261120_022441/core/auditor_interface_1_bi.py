import os
import re
from bs4 import BeautifulSoup

# ==============================================================================
# SCRIPT DE AUDITORIA E INTELIGÊNCIA SOVEREIGN ELITE (v5.3)
# Avaliação de Maturidade e Progresso da Interface para Padrão de 1 Bilhão de Dólares
# ==============================================================================

# Códigos de Cores ANSI para o Terminal
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def encontrar_arquivo_html():
    # Procura pelo index.html recursivamente em todas as subpastas do projeto
    for root, dirs, files in os.walk("."):
        if "index.html" in files:
            return os.path.join(root, "index.html")
    return None

def analisar_painel_sovereign():
    print(f"{CYAN}==================================================================")
    print("  THIERRY TECHNOLOGY CONCEPT GLOBAL - AUDITORIA DE ELITE (v5.3)   ")
    print(f"=================================================================={RESET}")
    
    html_path = encontrar_arquivo_html()
    
    if not html_path:
        print(f"{RED}[AVISO] Ficheiro 'index.html' não foi encontrado em nenhuma pasta do projeto.{RESET}")
        return

    print(f"{CYAN}[INFO] Ficheiro localizado com sucesso em: {html_path}{RESET}")

    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Critérios de verificação do cronograma de elite
    tem_glassmorphism = False
    tem_css_externo = False
    kernel_isolado = False
    padding_botoes = False
    
    # 1. Verificar injeção de CSS externo (sovereign-elite.css)
    links = soup.find_all("link", rel="stylesheet")
    for link in links:
        href = link.get("href")
        href_str = str(href) if href else ""
        if "sovereign-elite.css" in href_str:
            tem_css_externo = True
            break

    # 2. Verificar elementos no HTML e estilos inline/classes
    html_content = str(soup)
    if "backdrop-filter" in html_content or tem_css_externo:
        tem_glassmorphism = True
        
    if "max-height" in html_content or "overflow-y" in html_content:
        kernel_isolado = True

    if "padding" in html_content or "gap" in html_content:
        padding_botoes = True

    # Sistema de Pontuação Dinâmica (0 a 100)
    pontos = 20  # Base por existir a estrutura
    if tem_css_externo: pontos += 30
    if tem_glassmorphism: pontos += 20
    if kernel_isolado: pontos += 15
    if padding_botoes: pontos += 15

    # Função auxiliar para formatar status com cores
    def status_tag(condicao):
        if condicao:
            return f"{GREEN}[ CONCLUÍDO ]{RESET}"
        else:
            return f"{RED}[ PENDENTE ]{RESET}"

    # Relatório de Fases Concluídas
    print(f"\n{CYAN}[STATUS] Nível de Maturidade da Interface: {YELLOW}{pontos}/100{RESET}\n")
    print("FASES DO CRONOGRAMA IDENTIFICADAS:")
    print(f"{status_tag(tem_css_externo)} Etapa 1: Blindagem e Estética Global (Glassmorphism / CSS Externo)")
    print(f"{status_tag(kernel_isolado)} Etapa 2: Reestruturação Cirúrgica do Kernel e Limpeza de Logs")
    print(f"{status_tag(padding_botoes)} Etapa 3: Refinamento do Grid Biométrico e Painel de Comando")
    print(f"{status_tag(pontos >= 90)} Etapa 4: Prontidão Executiva para Demonstração Global (Vale do Silício)")

    print(f"\n{CYAN}------------------------------------------------------------------{RESET}")
    if pontos < 100:
        print(f"{YELLOW}O QUE FALTA PARA ATINGIR O PADRÃO DE 1 BILHÃO DE DÓLARES:{RESET}")
        if not tem_css_externo:
            print(f"  {RED}• Injetar a folha de estilos 'sovereign-elite.css' no <head> do ficheiro HTML encontrado.{RESET}")
        if not kernel_isolado:
            print(f"  {RED}• Aplicar rolagem interna e restrição de altura no bloco de Kernel Logs.{RESET}")
        if not padding_botoes:
            print(f"  {RED}• Otimizar o espaçamento e os micro-feedbacks dos botões de comando lateral.{RESET}")
    else:
        print(f"{GREEN}PARABÉNS! A interface atingiu o padrão máximo de elite do Vale do Silício.{RESET}")
    print(f"{CYAN}=================================================================={RESET}")

if __name__ == "__main__":
    analisar_painel_sovereign()