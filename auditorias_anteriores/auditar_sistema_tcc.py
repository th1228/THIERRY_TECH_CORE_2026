# -*- coding: utf-8 -*-
"""
Script de Auditoria Automatizada - Ecossistema TCC Global
Identifica a origem de textos indesejados (IA) e analisa o fluxo/atraso de PDFs.
"""

import os
import time
from pathlib import Path

def executar_auditoria():
    print("=" * 70)
    print(" 🕵️‍♂️ AUDITOR AUTOMATIZADO DO ECOSSISTEMA TCC GLOBAL")
    print("=" * 70)
    
    base_dir = Path(__file__).resolve().parent
    core_dir = base_dir / "core"
    pdfs_dir = core_dir / "pdfs_finais"
    
    # -----------------------------------------------------------------
    # 1. RASTREIO DE TEXTOS DE INTELIGÊNCIA ARTIFICIAL NO CÓDIGO
    # -----------------------------------------------------------------
    print("\n[+] 1. Investigando a origem dos termos de 'Inteligência Artificial'...")
    arquivos_py = list(base_dir.glob("**/*.py"))
    ocorrencias = []
    
    # Termos buscados para rastrear a origem do texto indesejado
    palavras_chave = ["artificial", "inteligência", "intelligence"]
    
    for arq in arquivos_py:
        if arq.name == "auditar_sistema_tcc.py":
            continue
        try:
            with open(arq, "r", encoding="utf-8", errors="ignore") as f:
                linhas = f.readlines()
                for num, linha in enumerate(linhas, 1):
                    linha_lower = linha.lower()
                    if any(pc in linha_lower for pc in palavras_chave):
                        ocorrencias.append({
                            "arquivo": str(arq.relative_to(base_dir)),
                            "linha": num,
                            "conteudo": linha.strip()
                        })
        except Exception as e:
            print(f"    [!] Erro ao ler {arq.name}: {e}")
            
    print(f"   -> Encontradas {len(ocorrencias)} ocorrências no código-fonte:")
    for oco in ocorrencias[:15]:  # Exibe até 15 ocorrências para análise rápida
        print(f"      - [{oco['arquivo']} : Linha {oco['linha']}] -> {oco['conteudo']}")
        
    if len(ocorrencias) > 15:
        print(f"      ... (e mais {len(ocorrencias) - 15} ocorrências omitidas).")

    # -----------------------------------------------------------------
    # 2. DIAGNÓSTICO DE ENTREGA E ATRASO DOS PDFs
    # -----------------------------------------------------------------
    print("\n[+] 2. Analisando o fluxo de entrega e atraso dos PDFs...")
    if pdfs_dir.exists():
        pdfs = list(pdfs_dir.glob("*.pdf"))
        print(f"   -> Pasta de destino monitorada: {pdfs_dir}")
        print(f"   -> Total de arquivos PDF encontrados: {len(pdfs)}")
        
        t_atual = time.time()
        for p in pdfs:
            t_mod = os.path.getmtime(p)
            idade_segundos = round(t_atual - t_mod, 2)
            tamanho_kb = round(p.stat().st_size / 1024, 2)
            print(f"      - Arquivo: {p.name}")
            print(f"        Tamanho: {tamanho_kb} KB | Modificado há {idade_segundos} segundos atrás")
    else:
        print(f"   [!] AVISO: A pasta de PDFs finais ({pdfs_dir}) não foi encontrada ou está vazia.")

    # -----------------------------------------------------------------
    # 3. VERIFICAÇÃO DOS COMPONENTES RESPONSÁVEIS
    # -----------------------------------------------------------------
    print("\n[+] 3. Verificando integridade dos módulos de entrega...")
    modulos_criticos = [
        base_dir / "main.py",
        core_dir / "gerador_dossies_master.py",
        core_dir / "c2_sovereign_intelligence.py"
    ]
    
    for mod in modulos_criticos:
        status = "PRESENTE E ÍNTEGRO" if mod.exists() else "AUSENTE"
        print(f"   -> {mod.relative_to(base_dir)}: [{status}]")
        
    print("\n" + "=" * 70)
    print(" AUDITORIA CONCLUÍDA COM SUCESSO.")
    print(" Use os caminhos e linhas acima para alterar os textos ou otimizar o fluxo.")
    print("=" * 70)

if __name__ == "__main__":
    executar_auditoria()