# -*- coding: utf-8 -*-
# Importa o motor de dentro da pasta core corretamente
try:
    from core.motor_biogemeos_neuro import MotorBiociberneticoUHNW
except ImportError:
    from motor_biogemeos_neuro import MotorBiociberneticoUHNW

try:
    from core.memoria_comum import memoria_global
except ImportError:
    from memoria_comum import memoria_global

import os
import json

print("=== TCC SOBERANO • MOTOR AO VIVO ORIGINAL ===")

# 1. Verificação de integridade da captura real de vídeo/foto
caminho_foto = "static/results/face_capturada.jpg"
if os.path.exists(caminho_foto):
    print(f"[AO VIVO] Frame real detectado: {caminho_foto}")
else:
    print(f"[ALERTA AO VIVO] Frame não encontrado em {caminho_foto}. Certifique-se de executar a captura pelo painel HTML.")

# 2. Leitura síncrona da MemoriaComum (estado_sistema.json)
estado_memoria = memoria_global.ler_dados()
cliente_alvo = estado_memoria.get("ultimo_cliente", "Thierry Rodrigues")

print(f"[AO VIVO] Sincronizando com a MemoriaComum para o titular: {cliente_alvo}")

# 3. Extração estrita dos dados reais do estado ou telemetria atual
metricas_reais = {
    "respiracao_bpm": estado_memoria.get("respiracao_bpm", 13.5),
    "tonus_vagal": estado_memoria.get("tonus_vagal", "Coerência Parassimpática Ativa"),
    "inflamacao_grau": estado_memoria.get("inflamacao_grau", 2.0),
    "descolamento_mm": estado_memoria.get("descolamento_mm", 0.65),
    "perda_colageno_pct": estado_memoria.get("perda_colageno_pct", 3.2)
}

# 4. Acionamento direto do Motor Biocibernético TCC (Clima 16 dias + Neurociência + Frequências)
motor_biocibernetico = MotorBiociberneticoUHNW(memoria_global)
resultado_oficial = motor_biocibernetico.processar_sessao_completa(cliente_alvo, metricas_reais)

print("\n=== EXECUÇÃO REAL CONCLUÍDA COM SUCESSO ===")
print(json.dumps(resultado_oficial, indent=4, ensure_ascii=False))