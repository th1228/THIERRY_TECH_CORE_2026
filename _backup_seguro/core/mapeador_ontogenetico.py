# -*- coding: utf-8 -*-
# =====================================================================
# THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026
# MIBO SOVEREIGN INTELLIGENCE - MAPEADOR & TELEMETRIA PSIQUICA DINÂMICA
# Versão: 2.2.0 - Dynamic Runtime Inspector & Ontogenetic Mapping
# =====================================================================

import os
import sys
from pathlib import Path

# Garante que o Python enxergue a raiz do projeto e o diretório core
script_dir = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.abspath(os.path.join(script_dir, "..")) if "core" in script_dir else script_dir
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

core_dir = os.path.join(raiz_projeto, "core")
if core_dir not in sys.path:
    sys.path.append(core_dir)

# Tenta importar a memória comum para fazer a leitura dinâmica dos estados
try:
    from memoria_comum import instancia_memoria as memoria
    tem_memoria = True
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
        tem_memoria = True
    except ImportError:
        tem_memoria = False

# Cores ANSI para o padrão High-Tech
VERDE = "\033[92m"
AMARELO = "\033[93m"
CIANO = "\033[96m"
BRANCO = "\033[97m"
CINZA = "\033[90m"
MAGENTA = "\033[95m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

def inspecionar_estado_psiquico():
    """Lê os registos ativos da memória comum gerados pelo módulo psíquico."""
    if not tem_memoria:
        return "Indisponível (Memória comum não detetada no escopo atual)"
    
    status = memoria.ler_dados("PSICO_STATUS") or "Inativo / Aguardando Execução"
    laudo = memoria.ler_dados("laudo_psiquico") or "Nenhum laudo registado"
    frequencia = memoria.ler_dados("FREQUENCIA_SONICA") or "528.0"
    coerencia = memoria.ler_dados("COERENCIA_BIOGINICA") or "0.0000"
    
    return {
        "status": status,
        "laudo": laudo,
        "frequencia": frequencia,
        "coerencia": coerencia
    }

def desenhar_arvore_dinamica():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(VERDE + "=" * 105 + RESET)
    print(AMARELO + "   THIERRY TECHNOLOGY CONCEPT GLOBAL • MAPA DINÂMICO & TELEMETRIA PSIQUICA" + RESET)
    print(CIANO + "   INSPEÇÃO EM TEMPO REAL DO MOTOR DE ONTOGÊNESE BIOMÉTRICA" + RESET)
    print(VERDE + "=" * 105 + RESET + "\n")

    raiz = Path(raiz_projeto)
    print(f"{BRANCO}📁 Raiz do Projeto:{RESET} {CINZA}{raiz}{RESET}\n")

    # Recolhe os dados diretamente da memória do ecossistema
    telemetria = inspecionar_estado_psiquico()

    print(f"{BRANCO}[DIAGRAMA DA ÁRVORE DO ECOSSISTEMA & ESTADO ATIVO]:{RESET}")
    print(f" └── THIERRY_TECH_CORE_2026/")
    print(f"     ├── {CIANO}main.py{RESET} {CINZA}(Ponto de Entrada FastAPI - Porta 801){RESET}")
    print(f"     ├── {CIANO}biometria.py{RESET} {CINZA}(Fonte de Telemetria e Fatores de Perturbação){RESET}")
    print(f"     └── {AMARELO}core/{RESET}")
    print(f"         ├── c2_sovereign_intelligence.py {CINZA}(Núcleo C2){RESET}")
    print(f"         ├── mibo_adaptive_neural_core.py {CINZA}(Núcleo Neural Adaptativo){RESET}")
    print(f"         ├── mibo_security_sovereign.py  {CINZA}(Segurança Soberana){RESET}")
    print(f"         ├── mibo_quantum_shield.py      {CINZA}(Escudo Quântico){RESET}")
    print(f"         ├── {VERDE}modulo_psiquico.py{RESET} {BRANCO}ativo [{MAGENTA}{NEGRITO}\"FREQUÊNCIA DE DEUS\" - 528 Hz{RESET}{BRANCO}]{RESET}")
    print(f"         └── {AMARELO}storage/{RESET}")
    print(f"             └── {CINZA}sovereign_international_audit_*.log{RESET}")

    print("\n" + VERDE + "-" * 105 + RESET)
    print(MAGENTA + " 🧬 [TELEMETRIA DO MÓDULO PSÍQUICO EM TEMPO REAL]:" + RESET)
    if isinstance(telemetria, dict):
        print(f"    • Estado do Módulo   -> {BRANCO}{telemetria['status']}{RESET}")
        print(f"    • Frequência Sônica  -> {CIANO}{telemetria['frequencia']} Hz{RESET}")
        print(f"    • Coerência Biogênica-> {VERDE}{telemetria['coerencia']}{RESET}")
        print(f"    • Último Laudo       -> {AMARELO}\"{telemetria['laudo']}\"{RESET}")
    else:
        print(f"    • {telemetria}")
    print(VERDE + "-" * 105 + RESET + "\n")

if __name__ == "__main__":
    desenhar_arvore_dinamica()