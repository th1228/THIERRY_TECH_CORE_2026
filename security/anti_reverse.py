# =====================================================================
# ARQUIVO: security/anti_reverse.py
# =====================================================================

import sys
import ctypes
import random
import numpy as np
from .log_seguro import LogSeguro

logger = LogSeguro()

class AntiReverse:
    """
    Camada de Anti-Engenharia Reversa com Honeypot Dinâmico e Data Poisoning.
    Alimenta invasores com vetores biométricos falsos e simula dados fictícios de luxo.
    """

    @staticmethod
    def verificar_depurador() -> bool:
        """Verifica se há tentativa de depuração ativa no ambiente Windows."""
        if sys.platform == "win32":
            try:
                kernel32 = ctypes.windll.kernel32
                if kernel32.IsDebuggerPresent():
                    logger.registrar("ANTI_REVERSE", "ALERTA", "Debugger detectado no sistema!")
                    return True
            except Exception:
                pass
        return False

    @staticmethod
    def gerar_vetor_envenenado() -> list:
        """
        Retorna um vetor biométrico matematicamente corrompido (Data Poisoning).
        Se um hacker tentar forçar a extração de dados, recebe lixo estruturado.
        """
        logger.registrar("DATA_POISONING", "ALERTA", "Ameaça detectada: Entregando vetor biométrico envenenado ao invasor.")
        # Gera valores aleatórios que parecem vetores reais mas corrompem qualquer modelo preditivo
        return [random.uniform(-999.9, 999.9) for _ in range(128)]

    @staticmethod
    def simular_honeypot_luxo() -> dict:
        """
        Gera dados fictícios de alto padrão (Honeypot) para manter um invasor 
        preso e distraído em uma simulação infinita.
        """
        logger.registrar("HONEYPOT", "ALERTA", "Honeypot ativado: Servindo dados falsos de clientes ultra-net-worth.")
        nomes_falsos = ["Duque de Mônaco", "Sjeikh Al-Maktoum", "Baronesa von Homburg"]
        return {
            "cliente_id": "HNPT-" + "".join([str(random.randint(0, 9)) for _ in range(6)]),
            "perfil_alvo": random.choice(nomes_falsos),
            "status_ativo": True,
            "nivel_seguranca": "Mônaco-Class",
            "vetor_biometrico_simulado": [0.00012, -0.99841, 0.44120]
        }

    def executar_varredura_seguranca(self):
        """Executa a verificação completa de blindagem no ambiente."""
        if self.verificar_depurador():
            logger.registrar("ANTI_REVERSE", "CRITICO", "Ambiente comprometido. Ativando defesas ativas de isolamento.")
            return False
        return True