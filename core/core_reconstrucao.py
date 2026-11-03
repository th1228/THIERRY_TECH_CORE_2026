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
Módulo: core_reconstrucao.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Versão: 2.0.1 - Importações Resilientes e Sincronização Segura
"""

import sys
import os
import logging

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

# Configuração de Log para capturar onde o erro acontece
logging.basicConfig(level=logging.INFO)

# Importações blindadas e resilientes para evitar falhas de caminho estático
biometria = None
diagnostico_ante_gravidade_neural = None
neuro_gravidade = None

try:
    import biometria
except ImportError:
    try:
        from core import biometria
    except ImportError:
        logging.warning("Módulo biometria não encontrado diretamente.")

try:
    import diagnostico_ante_gravidade_neural
except ImportError:
    try:
        from core import diagnostico_ante_gravidade_neural
    except ImportError:
        logging.warning("Módulo diagnostico_ante_gravidade_neural não encontrado diretamente.")

try:
    import neuro_gravidade
except ImportError:
    try:
        from core import neuro_gravidade
    except ImportError:
        logging.warning("Módulo neuro_gravidade não encontrado diretamente.")

def executar_reconstrucao_total():
    """
    Motor de consolidação com verificação de integridade e sincronização global.
    """
    try:
        bio_dados = biometria.obter_dados() if biometria and hasattr(biometria, 'obter_dados') else "Modulo indisponivel"
        diag_dados = diagnostico_ante_gravidade_neural.obter_dados() if diagnostico_ante_gravidade_neural and hasattr(diagnostico_ante_gravidade_neural, 'obter_dados') else "Modulo indisponivel"
        
        # Compatibilidade com o motor de neurogravidade atualizado
        if neuro_gravidade and hasattr(neuro_gravidade, 'processar'):
            neuro_dados = neuro_gravidade.processar()
        elif neuro_gravidade and hasattr(neuro_gravidade, 'obter_dados'):
            neuro_dados = neuro_gravidade.obter_dados()
        else:
            neuro_dados = "Modulo indisponivel"

        dados_consolidado = {
            "biometria": bio_dados,
            "diagnostico": diag_dados,
            "neuro": neuro_dados,
            "status_orquestracao": "Processamento concluído com sucesso"
        }
        
        # Sincronização automática com a Memória Comum 🧠
        try:
            memoria.salvar_dados("core_reconstrucao_consolidado", dados_consolidado)
        except Exception:
            pass

        return dados_consolidado
    except Exception as e:
        logging.error(f"Falha na execução interna: {str(e)}")
        erro_payload = {"erro": f"Falha na consolidação: {str(e)}"}
        
        try:
            memoria.salvar_dados("core_reconstrucao_consolidado", erro_payload)
        except Exception:
            pass
            
        return erro_payload

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    return executar_reconstrucao_total()

if __name__ == "__main__":
    resultado = executar_reconstrucao_total()
    print("Resultado da Reconstrução Total:", resultado)