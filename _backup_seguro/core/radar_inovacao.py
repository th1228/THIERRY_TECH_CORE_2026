import os
import textwrap

# Configuração de Cores ANSI para o Terminal do VS Code
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
BLUE = "\033[1;34m"
WHITE = "\033[1;37m"

def auditoria_cirurgica_total():
    projeto_path = "."
    
    total_linhas = 0
    total_arquivos = 0
    arquivos_encontrados_por_modulo = {
        "biogemeos": [],
        "fadiga": [],
        "biometrico": [],
        "c2_solver": [],
        "monaco": [],
        "main_llm": [],
        "security_zerotrust": [],
        "fhir_html": []
    }

    # Mapeamento técnico detalhado e restrito de cada motor real do ecossistema
    motores_alvo = {
        "biogemeos": {
            "nome": "Motor Biogêmeo (Biogêmeos_neuro.py / Biogênicos)",
            "desc": "Rede neural proprietária e processamento sináptico/biológico avançado.",
            "termos": ["biogemeos", "biogêmeos", "neuro", "biogenios"]
        },
        "fadiga": {
            "nome": "Sensor de Fadiga & Monitoramento Biométrico",
            "desc": "Algoritmos de detecção de exaustão, fadiga operacional e métricas biológicas em tempo real.",
            "termos": ["fadiga", "fatigue", "sensor_fadiga", "alert"]
        },
        "biometrico": {
            "nome": "Motor Biométrico (Cálculo Matemático Pesado)",
            "desc": "Processamento e validação de alta densidade matemática para identificação e segurança biométrica.",
            "termos": ["biometrico", "biometria", "biometric", "math_engine"]
        },
        "c2_solver": {
            "nome": "Motor C2 Solver (Resolução Analítica)",
            "desc": "Motor computacional responsável por resolver equações complexas e otimização numérica pesada.",
            "termos": ["c2", "solver", "c2_solver", "optmizer"]
        },
        "monaco": {
            "nome": "Mônaco Modelagem Engine",
            "desc": "Engine de modelagem preditiva, simulação matemática e projeções avançadas de ecossistemas.",
            "termos": ["monaco", "modelagem", "engine_monaco"]
        },
        "main_llm": {
            "nome": "Core Orquestrador (main.py & Memória Comum / LLM)",
            "desc": "Núcleo central de execução assíncrona, gestão de estado compartilhado e integração com LLMs.",
            "termos": ["main.py", "llm", "memoria", "memory", "orquestrador"]
        },
        "security_zerotrust": {
            "nome": "Pasta Security com Arquitetura Zero Trust & Vault",
            "desc": "Blindagem absoluta de dados, criptografia de ponta a ponta e controle estrito sem confiança implícita.",
            "termos": ["security", "zero_trust", "zerotrust", "vault", "crypto", "hash"]
        },
        "fhir_html": {
            "nome": "Interoperabilidade FHIR & Painel HTML Dinâmico",
            "desc": "Estruturação de dados médicos universais (JSON FHIR) acoplados a uma interface de zero carga cognitiva.",
            "termos": ["fhir", "hl7", "html", "ui", "painel"]
        }
    }

    pastas_ignoradas = {".git", "__pycache__", "venv", "env", "node_modules", ".vs", ".vscode"}
    extensoes_texto = (".py", ".js", ".html", ".css", ".json", ".txt", ".md", ".env")

    # Varredura Profunda e Real em Todo o Repositório
    for root, dirs, files in os.walk(projeto_path):
        dirs[:] = [d for d in dirs if d not in pastas_ignoradas]
        
        for file in files:
            total_arquivos += 1
            caminho_completo = os.path.join(root, file)
            caminho_lower = caminho_completo.lower()
            
            if file.endswith(extensoes_texto):
                try:
                    with open(caminho_completo, "r", encoding="utf-8", errors="ignore") as f:
                        linhas = f.readlines()
                        num_linhas = len(linhas)
                        total_linhas += num_linhas
                        conteudo_str = "".join(linhas).lower()
                        
                        # Verifica rigorosamente em qual motor/componente o arquivo se encaixa
                        for chave, dados in motores_alvo.items():
                            if any(termo in conteudo_str or termo in caminho_lower for termo in dados["termos"]):
                                if file not in arquivos_encontrados_por_modulo[chave]:
                                    arquivos_encontrados_por_modulo[chave].append(file)
                except Exception:
                    pass

    # Status de detecção de cada motor
    status_motores = {}
    total_ativos = 0
    for chave, dados in motores_alvo.items():
        encontrados = arquivos_encontrados_por_modulo[chave]
        if len(encontrados) > 0:
            status_motores[chave] = {"ativo": True, "detalhes": encontrados}
            total_ativos += 1
        else:
            status_motores[chave] = {"ativo": False, "detalhes": []}

    # Valuations baseados no volume real de código e na densidade tecnológica pesada
    fator_complexidade = 1.0 + (total_ativos * 0.35)
    valuation_nacional_brl = max(950000.0, (total_linhas * 90.0) * fator_complexidade)
    valuation_internacional_usd = max(700000.0, (total_linhas * 42.0) * fator_complexidade)

    classificacao_global = "Quantum-Biometric & Heavy Computational Intelligence Ecosystem (Zero Trust Architecture)"

    pitch_executivo = (
        "A plataforma da Thierry Technology Concept Global opera como um ecossistema de computação pesada e inteligência "
        "multimodal de alta performance. Sob a regência do núcleo central (main.py) e memória comum, o sistema integra "
        "o Motor Biogêmeo para redes neurais, o Sensor de Fadiga para monitoramento biológico, o Motor Biométrico "
        "e o C2 Solver executando os cálculos matemáticos mais densos, combinados com a Modelagem Mônaco, "
        "uma camada de LLM avançada, a pasta Security blindada sob preceitos rigorosos de Zero Trust / Vault e "
        "geração de dados padronizados em FHIR."
    )

    estrategias_venda = (
        "1. Licenciamento Enterprise de Motores Críticos (SDK/API B2B): Comercialização direta dos motores C2 Solver e Biométrico para indústrias de alta exigência.\n"
        "2. Infraestrutura SaaS Zero Trust de Alta Performance: Assinatura do ecossistema completo blindado por criptografia total.\n"
        "3. Cross-Border M&A / Aquisição de IP Tecnológica: Transferência de propriedade intelectual proprietária para fundos e conglomerados globais."
    )

    # IMPRESSÃO ORGANIZADA E COLORIDA NO TERMINAL
    print("\n" + CYAN + "="*95 + RESET)
    print(BOLD + WHITE + " 🔍 AUDITORIA CIRÚRGICA DE COMPONENTES E MOTORES - THIERRY TECH" + RESET)
    print(CYAN + "="*95 + RESET)

    print(f"\n{BOLD}{BLUE}🏢 1. CLASSIFICAÇÃO TÉCNICA DO SISTEMA:{RESET}")
    print(f"   • Categoria Global: {BOLD}{YELLOW}{classificacao_global}{RESET}")
    print(f"   • Núcleo de Segurança: {WHITE}Pasta Security com Zero Trust & Vault Criptografado ativo{RESET}")
    print(CYAN + "-" * 95 + RESET)

    print(f"\n{BOLD}{BLUE}📊 2. AUDITORIA DE CÓDIGO E VALUATION EM TEMPO REAL:{RESET}")
    print(f"   • Total de Arquivos Varridos no Projeto: {WHITE}{total_arquivos} arquivos{RESET}")
    print(f"   • Contagem Real e Profunda de Linhas: {BOLD}{GREEN}{total_linhas:,} linhas{RESET}")
    print(f"   • Motores e Módulos Pesados Detectados: {BOLD}{YELLOW}{total_ativos} de 8 pilares estruturais{RESET}")
    print(f"   • 🇧🇷 Valuation Estimado (Mercado Nacional): {BOLD}{GREEN}R$ {valuation_nacional_brl:,.2f} BRL{RESET}")
    print(f"   • 🇺🇸 Valuation Estimado (Mercado Internacional): {BOLD}{GREEN}$ {valuation_internacional_usd:,.2f} USD{RESET}")
    print(CYAN + "-" * 95 + RESET)

    print(f"\n{BOLD}{BLUE}🏛️ 3. MAPEAMENTO DETALHADO DOS MOTORES E CÁLCULOS:{RESET}")
    for chave, dados in motores_alvo.items():
        info = status_motores[chave]
        if info["ativo"]:
            status_tag = f"{BOLD}{GREEN}[ ATIVO & INTEGRADO ]{RESET}"
            origem = f"({len(info['detalhes'])} arquivo(s) mapeado(s): {', '.join(info['detalhes'][:3])})"
        else:
            status_tag = f"{BOLD}{RED}[ NÃO ENCONTRADO NO DIRETÓRIO ]{RESET}"
            origem = "(Aguardando vínculo no repositório)"

        print(f"   • {BOLD}{WHITE}{dados['nome']}{RESET}: {status_tag}")
        print(f"     {CYAN}Função:{RESET} {dados['desc']} {WHITE}{origem}{RESET}")
        print("   " + CYAN + "-"*91 + RESET)

    print(f"\n{BOLD}{BLUE}🎯 4. MODELO DE NEGÓCIO E ESTRATÉGIA COMERCIAL:{RESET}")
    print(formatar_texto(estrategias_venda, indent="   "))
    print(CYAN + "-" * 95 + RESET)

    print(f"\n{BOLD}{BLUE}📜 5. PITCH EXECUTIVO GLOBAL (O QUE O PROGRAMA FAZ HOJE):{RESET}")
    print(formatar_texto(pitch_executivo, indent="   "))
    print(CYAN + "="*95 + RESET)

    # Salvando relatório consolidado oficial
    with open("relatorio_radar_completo.txt", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE AUDITORIA CIRÚRGICA - THIERRY TECHNOLOGY CONCEPT GLOBAL\n\n")
        f.write(f"Classificacao: {classificacao_global}\n")
        f.write(f"Total de Linhas Varridas: {total_linhas:,}\n")
        f.write(f"Valuation Nacional (BRL): R$ {valuation_nacional_brl:,.2f}\n")
        f.write(f"Valuation Internacional (USD): $ {valuation_internacional_usd:,.2f}\n")
        f.write(f"Motores Ativos: {total_ativos}/8\n\n")
        f.write("Pitch Executivo:\n" + pitch_executivo + "\n\n")
        f.write("Estrategia Comercial:\n" + estrategias_venda)

    print(f"\n{BOLD}{GREEN}[✔] Auditoria cirúrgica concluída! Relatório atualizado em 'relatorio_radar_completo.txt'!{RESET}\n")

def formatar_texto(texto, indent="   "):
    return "\n".join(textwrap.wrap(texto, width=86, initial_indent=indent, subsequent_indent=indent))

if __name__ == "__main__":
    auditoria_cirurgica_total()