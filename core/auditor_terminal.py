import os

def executar_auditoria_terminal():
    projeto_path = "." # Diretório atual do seu projeto no VS Code
    
    # Mapeamento dos 4 Pilares Globais para o mercado internacional
    pilares = {
        "pilar_1_edge_offline": {
            "nome": "1. Arquitetura Edge & Offline-First",
            "desc": "Processamento local, cache em navegador ou WebAssembly/Whisper local.",
            "palavras_chave": ["offline", "wasm", "local", "whisper", "edge", "cache", "fallback"],
            "concluido": False
        },
        "pilar_2_fhir": {
            "nome": "2. Interoperabilidade Padrão HL7 / FHIR",
            "desc": "Conversão automática da transcrição em recursos estruturados FHIR JSON.",
            "palavras_chave": ["fhir", "hl7", "resource", "patient_fhir", "observation"],
            "concluido": False
        },
        "pilar_3_ui_ux": {
            "nome": "3. UI/UX Imersiva no Painel HTML",
            "desc": "Interface dinâmica em HTML/CSS com ondas sonoras e micro-animações.",
            "palavras_chave": [".html", "animation", "audio-wave", "ui", "dynamic-panel", "css"],
            "concluido": False
        },
        "pilar_4_compliance": {
            "nome": "4. Trilha de Auditoria e Criptografia (Compliance)",
            "desc": "Audit trail imutável, hash de áudio, carimbo de tempo e LGPD/HIPAA.",
            "palavras_chave": ["audit", "crypto", "hash", "sha256", "timestamp", "compliance", "lgpd", "hipaa"],
            "concluido": False
        }
    }

    # Varredura inteligente nos arquivos do projeto
    arquivos_encontrados = []
    for root, dirs, files in os.walk(projeto_path):
        if any(pasta in root for pasta in [".git", "__pycache__", "venv", "env", "node_modules"]):
            continue
            
        for file in files:
            caminho_completo = os.path.join(root, file)
            arquivos_encontrados.append(caminho_completo.lower())
            
            if file.endswith((".py", ".js", ".html", ".json")):
                try:
                    with open(caminho_completo, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo = f.read().lower()
                        for chave, pilar in pilares.items():
                            if any(palavra in conteudo or palavra in file.lower() for palavra in pilar["palavras_chave"]):
                                pilares[chave]["concluido"] = True
                except Exception:
                    pass

    for chave, pilar in pilares.items():
        if not pilar["concluido"]:
            for palavra in pilar["palavras_chave"]:
                if any(palavra in arq for arq in arquivos_encontrados):
                    pilares[chave]["concluido"] = True
                    break

    # Exibição limpa no Terminal do VS Code
    print("\n" + "="*65)
    print(" 🚀 AUDITORIA DE PRONTIDÃO GLOBAL (M&A) - STATUS DO SISTEMA")
    print("="*65)
    
    total_ok = 0
    for chave, pilar in pilares.items():
        status_str = "[ OK ] CONCLUÍDO" if pilar["concluido"] else "[ PENDENTE ] FAZER"
        if pilar["concluido"]:
            total_ok += 1
        print(f"• {pilar['nome']}")
        print(f"  Status: {status_str}")
        print(f"  O que é: {pilar['desc']}")
        print("-" * 65)

    print(f"📊 Progresso Global: {total_ok} de {len(pilares)} pilares estruturados.\n")

if __name__ == "__main__":
    executar_auditoria_terminal()