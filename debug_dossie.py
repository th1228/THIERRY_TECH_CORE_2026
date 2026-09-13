from datetime import datetime, timedelta
import math

# Cole a classe BiogemDigital aqui mesmo para teste rápido
class BiogemDigital:
    @staticmethod
    def calcular_inteligencia_preditiva(v_esq: float, v_dir: float) -> dict:
        v_esq = max(0.01, min(1.0, v_esq))
        v_dir = max(0.01, min(1.0, v_dir))
        nivel_inflamacao = max(0.05, 1.0 - ((v_esq + v_dir) / 2.0))
        estresse_oxidativo_total = min(1.0, nivel_inflamacao * 1.3)
        tonus_parassimpatico = max(5.0, 100.0 - (nivel_inflamacao * 85.0))
        nivel_ansiedade = min(100.0, (nivel_inflamacao * 55.0 + (100.0 - tonus_parassimpatico) * 0.45) * 100)
        descolamento_gordura_osso_mm = 1.85 + (nivel_inflamacao * 2.4)
        nivel_agua_pele_percentual = max(15.0, 75.0 - (nivel_inflamacao * 45.0))
        taxa_reflectancia_pele = f"{v_esq * 100:.1f}%"
        duracao_tratamento_dias = 16
        unidades_aproximadas_toxina = int(22 + (v_esq * 14))
        data_atual = datetime.now()
        data_toxina_ideal = data_atual + timedelta(days=int(10 + (v_esq * 6)))
        data_janela_cirurgica = data_atual + timedelta(days=int(7 + (nivel_inflamacao * 4)))
        data_neurogenese = data_atual + timedelta(days=int(15 - (tonus_parassimpatico * 0.04)))
        fator_k = 0.02 + (estresse_oxidativo_total * 0.07)
        risco_degenerativo_3_anos = min(100.0, (estresse_oxidativo_total * 70.0 + (100.0 - tonus_parassimpatico) * 0.3))
        risco_paralisia_2_anos = min(100.0, (abs(v_esq - v_dir) * 75.0 + nivel_inflamacao * 25.0))
        
        prescricao_tratamento = [
            f"Protocolo de Reancoragem de Coxins (Ciclo de {duracao_tratamento_dias} Dias): Reancorar {descolamento_gordura_osso_mm:.2f}mm.",
            f"Terapia de Regeneração: Água na pele a {nivel_agua_pele_percentual:.1f}%.",
            f"Toxina Preventiva: {data_toxina_ideal.strftime('%d/%m/%Y')} com {unidades_aproximadas_toxina} Unidades."
        ]

        return {
            "ptose_atual_mm": descolamento_gordura_osso_mm,
            "nivel_agua_pele_percentual": nivel_agua_pele_percentual,
            "data_toxina_ideal": data_toxina_ideal.strftime("%d/%m/%Y"),
            "unidades_aproximadas_toxina": unidades_aproximadas_toxina,
            "risco_degenerativo_3_anos": risco_degenerativo_3_anos,
            "prescricao_tratamento": prescricao_tratamento
        }

if __name__ == "__main__":
    dados = BiogemDigital.calcular_inteligencia_preditiva(0.70, 0.75)
    print("\n--- RESULTADO DIRETO DO MOTOR ---")
    for k, v in dados.items():
        print(f"{k}: {v}")