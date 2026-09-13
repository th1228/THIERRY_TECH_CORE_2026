# =====================================================================
# CAMADA 10: BEHAVIOR MONITOR / WAF LOCAL - TTC GLOBAL
# =====================================================================

class BehaviorMonitor:
    # Padrões suspeitos de comportamento anômalo em tempo de execução
    _padroes_anomalos = ["DROP TABLE", "EXEC(", "SYS_EXEC", "<SCRIPT>"]

    @staticmethod
    def inspecionar_comportamento(dados):
        """Inspeciona o payload em busca de desvios e comportamento malicioso."""
        print("[Camada 10] BehaviorMonitor: Inspecionando anomalias de execução...")
        
        payload_str = str(dados).upper()
        for padrao in BehaviorMonitor._padroes_anomalos:
            if padrao in payload_str:
                raise RuntimeError(f"BehaviorAnomalyDetected: Padrão malicioso detectado em tempo de execução: {padrao}")
        
        print("[Camada 10] BehaviorMonitor OK: Comportamento dentro dos parâmetros normais.")
        return True