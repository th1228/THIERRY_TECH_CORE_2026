# -*- coding: utf-8 -*-
# =====================================================================
# THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026
# MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - MIGRATOR & AUDITOR DE INTEGRIDADE
# =====================================================================

import os
import ast
from pathlib import Path

# Cores ANSI para o padrão High-Tech
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
CIANO = "\033[96m"
BRANCO = "\033[97m"
CINZA = "\033[90m"
RESET = "\033[0m"

def verificar_sintaxe_projeto(raiz: Path) -> list:
    """Verifica se todos os arquivos Python do projeto compilam sem erros de sintaxe."""
    erros_sintaxe = []
    for arquivo in raiz.glob("**/*.py"):
        if any(p in arquivo.parts for p in [".git", "__pycache__", "venv", "env", "node_modules"]):
            continue
        try:
            conteudo = arquivo.read_text(encoding="utf-8")
            ast.parse(conteudo, filename=str(arquivo))
        except Exception as e:
            erros_sintaxe.append(f"{arquivo.relative_to(raiz)}: {e}")
    return erros_sintaxe

def executar_migracao_e_diagnostico() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(VERDE + "=" * 85 + RESET)
    print(AMARELO + "   THIERRY TECHNOLOGY CONCEPT GLOBAL • MIGRADOR & AUDITOR DE INTEGRIDADE" + RESET)
    print(CIANO + "   ORGANIZAÇÃO SEGURA PARA PASTA CORE & VALIDAÇÃO COMPLETA DO SISTEMA" + RESET)
    print(VERDE + "=" * 85 + RESET + "\n")

    raiz = Path(".").resolve()
    pasta_core = raiz / "core"
    
    # 1. Criação segura da pasta core e pacote Python
    try:
        pasta_core.mkdir(parents=True, exist_ok=True)
        init_core = pasta_core / "__init__.py"
        if not init_core.exists():
            init_core.write_text("# Pacote Core do Ecossistema Thierry Technology Concept Global\n", encoding="utf-8")
    except Exception as e:
        print(f"{VERMELHO}[ERRO CRÍTICO]{RESET} Falha ao preparar a pasta 'core/': {e}")
        return

    modulos_para_mover = [
        "mibo_auto_optimizer.py",
        "mibo_deep_valuation_engine.py",
        "mibo_diagnostic.py",
        "mibo_master_control.py",
        "mibo_predictive_diagnostic.py",
        "mibo_status_geral.py",
        "mibo_structure_auditor.py",
        "monaco_ambiente.py",
        "monaco_blindagem.py",
        "monaco_comunicacao.py",
        "monaco_consciencia.py",
        "monaco_core_final.py",
        "monaco_eminencia.py",
        "monaco_integrador.py",
        "monaco_nucleo_acesso.py",
        "monaco_plan.py",
        "monaco_ressonancia.py"
    ]

    print(f"{BRANCO}[1/3] A mover módulos soltos da raiz para a pasta 'core/'...{RESET}")
    movidos = 0
    ja_no_lugar = 0
    erros_movimentacao = []

    for nome_arq in modulos_para_mover:
        origem = raiz / nome_arq
        destino = pasta_core / nome_arq

        if origem.exists():
            try:
                origem.rename(destino)
                print(f"  {VERDE}[MOVIDO]{RESET} {nome_arq} -> core/{nome_arq}")
                movidos += 1
            except Exception as e:
                print(f"  {VERMELHO}[FALHA]{RESET} {nome_arq}: {e}")
                erros_movimentacao.append(f"{nome_arq}: {e}")
        elif destino.exists():
            ja_no_lugar += 1
        else:
            print(f"  {CINZA}[NÃO ENCONTRADO]{RESET} {nome_arq} (não existe na raiz nem em core/)")

    print(f"\n{BRANCO}[2/3] A verificar o módulo de segurança (Quantum Shield)...{RESET}")
    shield_correto = (raiz / "security" / "mibo_quantum_shield.py").exists()
    if shield_correto:
        print(f"  {VERDE}[ OK ]{RESET} security/mibo_quantum_shield.py confirmado e blindado.")
    else:
        print(f"  {AMARELO}[AVISO]{RESET} security/mibo_quantum_shield.py não encontrado no caminho esperado.")

    print(f"\n{BRANCO}[3/3] A executar varredura de sintaxe em todo o ecossistema...{RESET}")
    erros_sintaxe = verificar_sintaxe_projeto(raiz)

    # =====================================================================
    # RELATÓRIO FINAL CONSOLIDADO NO TERMINAL
    # =====================================================================
    tudo_ok = (len(erros_movimentacao) == 0) and (len(erros_sintaxe) == 0) and shield_correto

    print("\n" + VERDE + "=" * 85 + RESET)
    print(AMARELO + "                    RESULTADO FINAL E SITUAÇÃO DO PROGRAMA" + RESET)
    print(VERDE + "=" * 85 + RESET)
    print(f" • Módulos movidos agora para 'core/'      : {VERDE}{movidos}{RESET}")
    print(f" • Módulos que já estavam em 'core/'      : {CIANO}{ja_no_lugar}{RESET}")
    print(f" • Erros durante a movimentação           : {VERMELHO if erros_movimentacao else VERDE}{len(erros_movimentacao)}{RESET}")
    print(f" • Quantum Shield em 'security/'          : {VERDE + 'OK (Ativo)' if shield_correto else VERMELHO + 'Pendente'}{RESET}")
    print(f" • Erros de sintaxe nos arquivos Python   : {VERMELHO if erros_sintaxe else VERDE}{len(erros_sintaxe)}{RESET}")
    print(VERDE + "-" * 85 + RESET)

    if erros_movimentacao:
        print(VERMELHO + " [!] DETALHES DOS ERROS DE MOVIMENTAÇÃO:" + RESET)
        for err in erros_movimentacao:
            print(f"   - {err}")

    if erros_sintaxe:
        print(VERMELHO + " [!] DETALHES DOS ERROS DE SINTAXE ENCONTRADOS:" + RESET)
        for err in erros_sintaxe:
            print(f"   - {err}")

    if tudo_ok:
        print(f"\n {VERDE}✅ SITUAÇÃO DO PROGRAMA: TUDO OK! SISTEMA ÍNTEGRO E ORGANIZADO.{RESET}")
    else:
        print(f"\n {AMARELO}⚠️ SITUAÇÃO DO PROGRAMA: ATENÇÃO NECESSÁRIA NOS PONTOS ACIMA.{RESET}")
    print(VERDE + "=" * 85 + RESET + "\n")

if __name__ == "__main__":
    resp = input("Deseja iniciar a organização segura e o diagnóstico final do sistema? (s/n): ")
    if resp.strip().lower() == 's':
        executar_migracao_e_diagnostico()
    else:
        print("Operação cancelada.")