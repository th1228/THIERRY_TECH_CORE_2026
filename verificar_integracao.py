# -*- coding: utf-8 -*-
import os
import json

def verificar_ecossistema():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print(" DIAGNÓSTICO DE INTEGRAÇÃO DO ECOSSISTEMA TTC GLOBAL")
    print("=" * 60)
    
    # Lista de componentes críticos para verificar
    componentes = {
        "Núcleo / Fila (Memória Comum)": os.path.join(base_dir, "core", "memoria_comum.py"),
        "Segurança (Portaria)": os.path.join(base_dir, "security", "portaria.py"),
        "Motor de Criptografia": os.path.join(base_dir, "security", "crypto_engine.py"),
        "Servidor Central (Main)": os.path.join(base_dir, "main.py"),
        "Interface Web (Painel HTML)": os.path.join(base_dir, "painel_web.html"),
        "Licença Ativa": os.path.join(base_dir, "licenca_ativa.json"),
        "Scanner Biométrico": os.path.join(base_dir, "core", "biogemeo_scanner.py"),
        "Motor de Osteometria": os.path.join(base_dir, "core", "osteometria_script.py"),
        "Módulo de Clima": os.path.join(base_dir, "core", "script_clima.py"),
    }
    
    integrados = 0
    total = len(componentes)
    
    for nome, caminho in componentes.items():
        existe = os.path.exists(caminho)
        status = "[INTEGRADO & ATIVO]" if existe else "[AUSENTE / PENDENTE]"
        if existe:
            integrados += 1
        print(f" {status} -> {nome}")
        print(f"    Caminho: {caminho}")
        print("-" * 60)
        
    print(f"\n[RESUMO] Componentes integrados com sucesso: {integrados}/{total}")
    
    # Verifica o estado atual na memória comum, se existir
    estado_path = os.path.join(base_dir, "estado_sistema.json")
    if os.path.exists(estado_path):
        print("[ESTADO] Arquivo de estado compartilhado encontrado.")
        try:
            with open(estado_path, "r", encoding="utf-8") as f:
                dados = json.load(f)
                print(f"    Dados salvos na memória: {list(dados.keys()) if dados else 'Vazio'}")
        except:
            print("    [AVISO] Estado compartilhado consolidado ou ilegível.")
    else:
        print("[ESTADO] Nenhum estado compartilhado gravado ainda.")
    print("=" * 60)

if __name__ == "__main__":
    verificar_ecossistema()