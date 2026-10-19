import sys, os

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# -*- coding: utf-8 -*-
import time
from core.banco_dados import salvar_cliente

class ProcessadorInteligente:
    def __init__(self, lang: str = "PT"):
        self.historico = []
        self.memoria = None
        self.perimetro_seguranca = 100.0  # KM
        self.bloqueado = False

    def conectar_memoria(self, instancia_memoria):
        self.memoria = instancia_memoria
        print("[MOTOR] Memória integrada com sucesso.")

    def set_historico(self, dados_16_dias):
        self.historico = dados_16_dias

    def verificar_geodefense(self):
        """Monitora perimetro e bloqueios."""
        from memoria_comum import instancia_memoria as memoria
        if not self.memoria: self.memoria = memoria
        
        distancia = self.memoria.ler_dados("DISTANCIA_ATUAL")
        if distancia and distancia >= self.perimetro_seguranca:
            if not self.bloqueado:
                print("[ALERTA CRÍTICO] Perímetro de 100km atingido.")
                self.memoria.receber_dados("STATUS_SISTEMA", "BLOQUEADO")
                self.bloqueado = True
                salvar_cliente("GEODEFENSE_TRIGGER", 0.0, "BLOQUEIO_100KM")

    def analisar_estado_atual(self, bio, feedback, osteo):
        """Processa os inputs e gera o parecer estratégico."""
        from memoria_comum import instancia_memoria as memoria
        if not self.memoria: self.memoria = memoria
        
        score_atual = (bio.get('estabilidade', 0) * 0.4) + (feedback * 0.3) + (osteo.get('melhora', 0) * 0.3)
        melhor_dia = self._encontrar_dia_mais_semelhante(bio)
        
        if melhor_dia is None: 
            return {"status": "Aguardando histórico..."}
            
        parecer = self._gerar_parecer(melhor_dia, score_atual)
        if self.memoria: 
            self.memoria.receber_dados("PARECER_ESTRATEGICO", parecer)
        return parecer

    def _encontrar_dia_mais_semelhante(self, bio_atual):
        if not self.historico: return None
        # Simula busca de padrões no histórico
        return min(self.historico, key=lambda dia: abs(dia['bio']['pressao'] - bio_atual.get('pressao', 0)))

    def _gerar_parecer(self, referencia, score):
        """Gera a análise estratégica com as frases de longevidade."""
        parecer = {
            "decisao_estrategica": {
                "acao": "Intervenção osteométrica e neuroolfativa de efeito gravitacional",
                "sistema": "Sistema límbico e regenerativo para longevidade ativo",
                "lado": referencia.get('lado', 'ND'), 
                "cor": referencia.get('cor', 'ND')
            },
            "protocolo_limbico": {
                "massagem": referencia.get('massagem', 'padrao'), 
                "musica": referencia.get('musica', 'padrao'), 
                "frequencia": referencia.get('frequencia', 0)
            },
            "status_regeneracao": "APICE" if score > 8.5 else "EM_CURSO"
        }
        
        # Impressão obrigatória para confirmação no terminal
        print(f"\n[MOTOR DE DECISÃO] STATUS: {parecer['decisao_estrategica']['acao']} | {parecer['decisao_estrategica']['sistema']}\n")
        
        return parecer

    def iniciar_processamento(self):
        """Loop principal do motor."""
        print("[MOTOR] Processamento estratégico e Geodefense ativos.")
        while True:
            # O motor realiza verificações constantes aqui
            self.verificar_geodefense()
            time.sleep(5) # Intervalo aumentado para otimização de CPU