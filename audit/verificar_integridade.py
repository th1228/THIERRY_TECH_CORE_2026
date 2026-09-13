import os
from pathlib import Path

def verificar_integridade():
    root = Path(__file__).resolve().parent
    arquivos_esperados = {
        "architecture_auditor.py": "class ArchitectureAuditor",
        "sovereign_auditor.py": "class SovereignEnterpriseAuditor",
        "auditor_geral_ttc.py": "run_full_audit",
        "privacy_auditor.py": "class PrivacyAuditor",
        "develops_readiness.py": "audit_devops",
        "dependency_sbom.json": "sbom_version",
        "license_compliance.json": "sbom_version",
        "dossie_executivo_global.md": "DOSSIÊ EXECUTIVO SOBERANO",
        "security_policy.md": None
    }

    print("=== INICIANDO VALIDAÇÃO DE INTEGRIDADE DA PASTA AUDIT ===\n")
    erros = 0

    for arq, assinatura in arquivos_esperados.items():
        caminho = root / arq
        if not caminho.exists():
            print(f"[-] ERRO: O arquivo '{arq}' está faltando na pasta audit/.")
            erros += 1
            continue
            
        conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
        
        if len(conteudo.strip()) == 0:
            print(f"[-] ERRO: O arquivo '{arq}' está vazio.")
            erros += 1
            continue

        if assinatura and assinatura not in conteudo:
            print(f"[-] AVISO: '{arq}' não contém a assinatura esperada ('{assinatura}').")
            erros += 1
        else:
            print(f"[+] OK: {arq:<30} -> Íntegro e estruturado corretamente.")

    print("\n--------------------------------------------------")
    if erros == 0:
        print("[SUCESSO] Todos os arquivos da auditoria estão perfeitos e sem sobreposições!")
    else:
        print(f"[ATENÇÃO] Foram encontrados {erros} pontos para revisar.")

if __name__ == "__main__":
    verificar_integridade()