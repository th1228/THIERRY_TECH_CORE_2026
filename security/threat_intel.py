# =====================================================================
# CAMADA 12: THREAT INTELLIGENCE (REPUTAÇÃO E ORIGEM) - TTC GLOBAL
# =====================================================================

class ThreatIntel:
    @staticmethod
    def verificar_reputacao(dados):
        print("[Camada 12] ThreatIntel: Consultando bases de reputação e ameaças...")
        if "BLACKED_IP" in str(dados).upper():
            raise PermissionError("ThreatIntelAlert: Origem associada a indicadores de comprometimento.")
        print("[Camada 12] ThreatIntel OK: Nenhuma ameaça conhecida na origem.")
        return True