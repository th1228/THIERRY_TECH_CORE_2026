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
"""
Módulo: auto_reparador.py
Descrição: Varredura inteligente com reinício automático a partir do ponto de paragem (ignora o que já está limpo).
"""

import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


def refatorar_ficheiro(caminho_arquivo: Path, client: genai.Client) -> tuple[bool, str]:
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            codigo_original = f.read()
    except Exception as e:
        return False, f"Erro de leitura: {e}"

    # Se já estiver limpo, não faz nada
    if "except:" not in codigo_original and "except Exception" not in codigo_original:
        return False, "Já limpo anteriormente"

    prompt = f"""
    Você é um Arquiteto de Software Sênior em Python e Especialista em Segurança.
    O código abaixo contém blocos `except:` ou `except Exception:` genéricos.
    
    Sua missão:
    1. Substitua os excepts genéricos por exceções específicas baseadas no contexto (ex: ValueError, KeyError, FileNotFoundError, ConnectionError, etc.) ou adicione tratamento adequado sem ocultar erros críticos.
    2. NUNCA altere as assinaturas de funções, regras de negócio ou lógica de cálculo.
    3. Mantenha todos os comentários e docstrings intactos.

    IMPORTANTE: Retorne APENAS o código Python corrigido dentro de um bloco markdown (```python ... ```).

    === CÓDIGO ORIGINAL ({caminho_arquivo.name}) ===
    ```python
    {codigo_original}
    ```
    """

    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            texto_resposta = response.text

            if not texto_resposta:
                return False, "Resposta vazia da IA"

            if "```python" in texto_resposta:
                codigo_novo = texto_resposta.split("```python")[1].split("```")[0].strip()
            elif "```" in texto_resposta:
                codigo_novo = texto_resposta.split("```")[1].split("```")[0].strip()
            else:
                codigo_novo = texto_resposta.strip()

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(codigo_novo + "\n")
                
            return True, "Substituição de exceções genéricas por específicas concluída com sucesso."
        
        except Exception as e:
            erro_str = str(e)
            if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                if tentativa < max_tentativas - 1:
                    tempo_espera = 25 * (tentativa + 1)
                    print(f"    ⏳ Limite de quota atingido. A aguardar {tempo_espera}s para retomar...")
                    time.sleep(tempo_espera)
                    continue
            return False, f"Erro na API: {e}"

    return False, "Falha após esgotar tentativas de contorno de quota."


def varrer_e_reparar_projeto(diretorio_base: Path, client: genai.Client) -> None:
    print(f"🚀 Iniciando recuperação e varredura inteligente a partir de: {diretorio_base.resolve()}\n")
    
    pastas_ignoradas = {".git", ".venv", "venv", "__pycache__", ".idea", "build", "dist"}
    todos_arquivos = [p for p in diretorio_base.rglob("*.py") if not any(ign in p.parts for ign in pastas_ignoradas) and p.name != "auto_reparador.py"]
    
    total_encontrados = len(todos_arquivos)
    print(f"📁 Total de ficheiros Python no projeto: {total_encontrados}")
    print("🔍 Verificando estado dos ficheiros (os já corrigidos serão ignorados automaticamente)...\n")
    print("=" * 80)

    relatorio = []
    sucessos = 0
    processados_ia = 0
    ignorados_automaticamente = 0

    for idx, caminho_arquivo in enumerate(todos_arquivos, 1):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()
        except:
            conteudo = ""

        # Verificação crucial: se o ficheiro NÃO tem exceções genéricas, ele já foi resolvido!
        if "except:" not in conteudo and "except Exception" not in conteudo:
            ignorados_automaticamente += 1
            continue

        print(f"[{idx}/{total_encontrados}] 🔧 Ficheiro pendente detetado - A processar com IA: {caminho_arquivo.name}...")
        alterado, mensagem = refatorar_ficheiro(caminho_arquivo, client)
        
        status = "OK" if alterado else "AVISO"
        if alterado:
            sucessos += 1
            
        relatorio.append({
            "arquivo": str(caminho_arquivo),
            "status": status,
            "detalhe": mensagem
        })
        
        processados_ia += 1
        # Pausa preventiva para evitar disparar novos erros de quota
        time.sleep(4)

    print("\n" + "=" * 80)
    print("📊 RELATÓRIO CONSOLIDADO DE AUTO-REPARAÇÃO")
    print("=" * 80)
    print(f"• Ficheiros já limpos anteriormente (ignorados): {ignorados_automaticamente}")
    print(f"• Ficheiros processados nesta ronda: {processados_ia}")
    print(f"• Ficheiros refatorados com sucesso agora: {sucessos}\n")
    
    for item in relatorio:
        print(f"• Ficheiro: {item['arquivo']}")
        print(f"  Status: [{item['status']}]")
        print(f"  Aprimoramento: {item['detalhe']}")
        print("-" * 80)

    print("\n🎯 Processo continuado e concluído com sucesso!")


if __name__ == "__main__":
    if not HAS_GENAI:
        print("❌ Instale a biblioteca correta: pip install google-genai")
        sys.exit(1)

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Chave de API não encontrada no ambiente nem no ficheiro .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    varrer_e_reparar_projeto(Path("."), client)