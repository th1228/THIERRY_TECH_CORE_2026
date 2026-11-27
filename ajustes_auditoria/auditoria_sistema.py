# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

# -*- coding: utf-8 -*-
import os
import sys
import ast
import json

# --- BLOCO DE CONEXÃO ESTRUTURAL ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from memoria_comum import instancia_memoria
except ImportError:
    instancia_memoria = None

class AuditoriaSistema:
    """
    Ferramenta de diagnóstico para mapear arquivos do projeto,
    verificar conexões com o main.py e integrar com a Memória Comum.
    """
    def __init__(self, diretorio_base="."):
        self.diretorio_base = diretorio_base
        self.pastas_ignoradas = {".git", "__pycache__", ".vscode", "venv", "env"}

    def listar_arquivos_python(self):
        """Varre a raiz e subpastas permitidas em busca de arquivos .py"""
        arquivos_py = []
        for raiz, dirs, arquivos in os.walk(self.diretorio_base):
            # Remove pastas que devem ser ignoradas
            dirs[:] = [d for d in dirs if d not in self.pastas_ignoradas]
            
            for arquivo in arquivos:
                if arquivo.endswith(".py"):
                    caminho_completo = os.path.join(raiz, arquivo)
                    arquivos_py.append(caminho_completo)
        return arquivos_py

    def analisar_conexoes_main(self, caminho_main="main.py"):
        """Analisa o main.py para identificar módulos importados"""
        modulos_importados = set()
        if not os.path.exists(caminho_main):
            return modulos_importados

        with open(caminho_main, "r", encoding="utf-8") as f:
            try:
                arvore = ast.parse(f.read(), filename=caminho_main)
                for no in ast.walk(arvore):
                    if isinstance(no, ast.Import):
                        for alias in no.names:
                            modulos_importados.add(alias.name.split(".")[0])
                    elif isinstance(no, ast.ImportFrom):
                        if no.module:
                            modulos_importados.add(no.module.split(".")[0])
            except Exception as e:
                print(f"[AUDITORIA] Erro ao analisar AST do main.py: {e}")
                
        return modulos_importados

    def executar_auditoria(self):
        """Executa a contagem, verificação e integração com a Memória Comum"""
        todos_arquivos = self.listar_arquivos_python()
        total_arquivos = len(todos_arquivos)
        
        modulos_main = self.analisar_conexoes_main()
        
        conexoes = []
        desconectados = []
        
        for arq in todos_arquivos:
            nome_base = os.path.basename(arq).replace(".py", "")
            pasta = os.path.basename(os.path.dirname(arq))
            
            if nome_base == "main" or nome_base == "auditoria_sistema":
                continue
                
            if nome_base in modulos_main or pasta in modulos_main:
                conexoes.append(arq)
            else:
                desconectados.append(arq)

        relatorio = {
            "total_arquivos_python": total_arquivos,
            "arquivos_conectados": len(conexoes),
            "arquivos_desconectados": desconectados,
            "status": "sucesso"
        }

        # Salva automaticamente na Memória Comum se disponível 💾
        if instancia_memoria is not None:
            instancia_memoria.salvar_dados("RELATORIO_AUDITORIA", relatorio)
            print("[AUDITORIA] Relatório salvo com sucesso na Memória Comum 🧠.")
        else:
            print("[AUDITORIA AVISO] Instância de memória comum não encontrada para salvar o estado.")

        return relatorio

if __name__ == "__main__":
    auditor = AuditoriaSistema()
    resultado = auditor.executar_auditoria()
    print(f"\n📊 Total de arquivos .py encontrados: {resultado['total_arquivos_python']}")
    print(f"🔗 Arquivos conectados estruturalmente: {resultado['arquivos_conectados']}")
    print(f"⚠️ Arquivos potencialmente desconectados: {len(resultado['arquivos_desconectados'])}")