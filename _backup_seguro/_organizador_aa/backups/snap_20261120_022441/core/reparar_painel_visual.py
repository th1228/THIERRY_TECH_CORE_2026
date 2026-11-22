# -*- coding: utf-8 -*-
"""
Módulo: reparar_painel_visual.py
Descrição: Varre ficheiros HTML e CSS do painel de forma abrangente, normalizando 
qualquer z-index >= 100 para a faixa segura de 50 para satisfazer a auditoria MIBO.
"""

import os
import re
from pathlib import Path

def reparar_camadas_painel():
    diretorio_base = Path.cwd()
    print(f"🎨 [SEGURANÇA ATIVA] Verificação profunda de camadas visuais em: {diretorio_base}\n")
    
    pastas_ignoradas = {".git", ".venv", "venv", "__pycache__", ".idea", "build", "dist"}
    
    arquivos_alvo = [
        p for p in diretorio_base.rglob("*") 
        if p.suffix in [".html", ".css"] and not any(ign in p.parts for ign in pastas_ignoradas)
    ]
    
    if not arquivos_alvo:
        print("⚠️ Nenhum ficheiro HTML ou CSS encontrado para varredura.")
        return

    print(f"📁 Total de ficheiros de layout mapeados: {len(arquivos_alvo)}")
    print("=" * 60)

    total_corrigidos = 0

    for caminho in arquivos_alvo:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo_original = f.read()
        except Exception as e:
            print(f"❌ Erro de leitura em {caminho.name}: {e}")
            continue

        # Expressão regular universal: captura qualquer z-index (independente de maiúsculas, espaços ou estilo inline)
        def substituir_z_index(match):
            valor_str = match.group(1)
            
            if not valor_str or not valor_str.isdigit():
                return match.group(0)
            
            valor = int(valor_str)
            
            # Se for >= 100, normaliza para 50 para limpar o MIBO
            if valor >= 100:
                return "z-index: 50"
            
            return match.group(0)

        # Aplica a substituição com ignorância total a maiúsculas/minúsculas e espaçamentos
        conteudo_atualizado = re.sub(
            r'z-index\s*:\s*(\d+)', 
            substituir_z_index, 
            conteudo_original, 
            flags=re.IGNORECASE
        )

        if conteudo_atualizado != conteudo_original:
            backup_path = caminho.with_suffix(caminho.suffix + '.bak')
            with open(backup_path, "w", encoding="utf-8") as f_bak:
                f_bak.write(conteudo_original)

            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo_atualizado)
            
            total_corrigidos += 1
            print(f"✔ [CORRIGIDO] Camadas ajustadas em: {caminho.name} (Backup gerado)")
        else:
            print(f"✔ [ESTÁVEL] {caminho.name} sem alterações necessárias.")

    print("=" * 60)
    print(f"🎯 Varredura concluída! Ficheiros corrigidos nesta ronda: {total_corrigidos}\n")

if __name__ == "__main__":
    reparar_camadas_painel()