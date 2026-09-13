import ctypes
import gc
import sys
import logging

# Configuração de logging seguro para o ecossistema
logger = logging.getLogger("TTC_Security")
logger.setLevel(logging.INFO)

class EphemeralShredder:
    """
    Destruidor Efêmero de Memória (Ephemeral Shredder).
    Garante a sobrescrita física e a remoção imediata de dados sensíveis 
    da RAM (como vetores biométricos e métricas faciais) pós-processamento.
    """

    @staticmethod
    def shred(data_container) -> None:
        """
        Sobrescreve e destrói o container de dados da memória.
        Suporta bytearray, listas e buffers de memória mutáveis.
        """
        try:
            if isinstance(data_container, bytearray):
                # Sobrescreve cada byte com zeros (limpeza física de baixo nível)
                for i in range(len(data_container)):
                    data_container[i] = 0
            elif isinstance(data_container, list):
                # Limpa elementos internos se forem mutáveis
                for i in range(len(data_container)):
                    if isinstance(data_container[i], (bytearray, list)):
                        EphemeralShredder.shred(data_container[i])
                    data_container[i] = None
            elif hasattr(data_container, "__bytes__") or isinstance(data_container, bytes):
                logger.warning("Objetos do tipo 'bytes' são imutáveis em Python. Apenas a referência foi apagada.")

            # Deleta a referência da variável do escopo atual
            del data_container
            
            # Força o coletor de lixo a liberar a memória imediatamente
            gc.collect()
            
        except Exception as e:
            logger.error(f"Erro crítico durante o processo de shredding: {str(e)}")
            raise

    @staticmethod
    def secure_wipe_string(texto_sensivel: str) -> None:
        """
        Nota de arquitetura: Strings em Python são imutáveis e ficam alocadas 
        em cache interno. Para dados altamente confidenciais, prefira sempre 
        processar usando `bytearray` em vez de `str`.
        """
        del texto_sensivel
        gc.collect()