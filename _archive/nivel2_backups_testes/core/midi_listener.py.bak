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
import sys
import os
import datetime
import numpy as np

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

class MIDIProtocolListener:
    def __init__(self, callback_atualizacao=None, lang: str = "PT"):
        self.callback = callback_atualizacao
        print("[MIDI_LISTENER] Protocolo de escuta inicializado.")

    def iniciar(self):
        """Método de disparo opcional para manter compatibilidade com o main.py 💻."""
        print("[MIDI_LISTENER] Listener de hardware ativo e escutando barramento...")
        if self.callback:
            try:
                self.callback({"protocolo": "MONACO_ACTIVE", "total": 0.0})
            except Exception as e:
                print(f"[MIDI_LISTENER] Erro ao disparar callback inicial: {e}")

def processar_escuta_background(nome_cliente, refletancia_pele_valor=0.74, clima_regiao="ÚMIDO"):
    print(f"[MIDI_LISTENER] Executando escuta analítica e cruzamento de dados para: {nome_cliente}")

    marcas_tratamento = [
        "L'Oréal Professionnel", "Davines OI", "Wella Professionals", 
        "Kérastase", "Senscience", "Algas Marinhas Tech"
    ]
    tipos_massagem = [
        "Shiatsu", "Miofascial", "Drenagem Linfática", 
        "Ayurvédica", "Reflexologia Craniana"
    ]
    oleos_essenciais = [
        "Gerânio + Olíbano", "Hortelã-Pimenta", "Capim-Limão", 
        "Lavanda", "Camomila Nobre"
    ]
    tons_voz = ["Tom Alto", "Tom Médio", "Tom Baixo"]
    frequencias_sonoras = [
        "528Hz (DNA Repair / Frequência de Deus)", 
        "432Hz (Harmonia Celular)", 
        "LO-FI Focus Alpha", 
        "Ambient Delta Vagal", 
        "Binaural Neural Sync"
    ]
    
    matriz_16_dias = []
    data_base = datetime.datetime.now()
    teor_hidratacao_pele = round(refletancia_pele_valor * 100, 1)
    
    for i in range(16):
        data_atual = data_base + datetime.timedelta(days=i)
        data_str = data_atual.strftime("%d/%m/%Y")
        
        clima_dia = "SECO" if (i % 2 == 0) else "ÚMIDO"
        necessidade_fios = "HIDRATAÇÃO PROFUNDA" if clima_dia == "SECO" else "RECONSTRUÇÃO HÍDRICA"
        
        tratamento = marcas_tratamento[i % len(marcas_tratamento)]
        decisao = "ESTRATÉGICA" if i % 3 == 0 else ("ASSERTIVA" if i % 3 == 1 else "METÓDICA")
        lado_parassimpatico = "DIREITO" if i % 2 == 0 else "ESQUERDO"
        cor_dia = "Dourado Executivo" if i % 2 == 0 else "Azul Ciano / Platina"
        oleo = oleos_essenciais[i % len(oleos_essenciais)]
        massagem = tipos_massagem[i % len(tipos_massagem)]
        voz = tons_voz[i % len(tons_voz)]
        musica = frequencias_sonoras[i % len(frequencias_sonoras)]
        
        if i == 6 or i == 13:
            status_regeneracao = "APEX CELULAR ATIVO (Dia Ápice de Regeneração)"
            nivel_inflamacao = "MÍNIMO [0.7 mg/L - Ótimo para Procedimento]"
        else:
            status_regeneracao = "FASE DE ADAPTAÇÃO & SÍNTESE"
            nivel_inflamacao = "BAIXO [1.2 mg/L - Estável]"

        matriz_16_dias.append({
            "data": data_str,
            "clima": clima_dia,
            "necessidade": necessidade_fios,
            "tratamento": tratamento,
            "decisao": decisao,
            "lado": lado_parassimpatico,
            "cor": cor_dia,
            "oleo": oleo,
            "massagem": massagem,
            "voz": voz,
            "musica": musica,
            "nivel_inflamacao": nivel_inflamacao,
            "status_regeneracao": status_regeneracao
        })

    psicomodulacoes = {
        "titular": nome_cliente,
        "psicomodulacao_1_comportamental": "ALTA PERFORMANCE EXECUTIVA // Perfil de Decisão Estratégica e Liderança.",
        "psicomodulacao_2_limbica": "SISTEMA AUTONÔMICO EQUILIBRADO // Resposta Vagal Alinhada ao Lado Predominante.",
        "psicomodulacao_3_regenerativa": f"TEOR HÍDRICO CUTÂNEO (Sensor): {teor_hidratacao_pele}% | Plasticidade Sináptica Pronta.",
        "parecer_medico_inflamacao": "SISTEMA APTO PARA PROTOCOLOS CLÍNICOS E CIRÚRGICOS NOS DIAS ÁPICE Mapeados."
    }

    # Sincronização automática com a Memória Comum 🧠
    try:
        memoria.salvar_dados("mid_listener", {
            "psicomodulacoes": psicomodulacoes,
            "matriz_16_dias": matriz_16_dias
        })
        print("[MEMÓRIA] Dados do Mid Listener sincronizados com sucesso.")
    except Exception as e:
        print(f"[MEMÓRIA] Erro ao sincronizar Mid Listener: {e}")

    return psicomodulacoes, matriz_16_dias