# =====================================================================
# CAMADA: DATA MASKING (OFUSCAÇÃO DE DADOS) - TTC GLOBAL
# =====================================================================

class DataMasking:
    @staticmethod
    def mascarar(dados):
        print("[Camada 11] DataMasking: Ofuscando dados sensíveis...")
        if isinstance(dados, str) and len(dados) > 6:
            dados_mascarados = dados[:3] + "****" + dados[-3:]
        else:
            dados_mascarados = "****"
        print(f"[Camada 11] Dados mascarados para log/transmissão: {dados_mascarados}")
        return dados_mascarados