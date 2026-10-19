# -*- coding: utf-8 -*-
import os
import json
import datetime
import psutil

CHECKLIST_FILE = "checklist_15_dias.json"

def executar_monitoramento():
    agora = datetime.datetime.now()
    data_hoje = agora.date()
    hora_hoje = agora.strftime("%H:%M:%S")

    cpu_geral = psutil.cpu_percent(interval=1)
    ram_pc = psutil.virtual_memory().percent

    print(f"\n--- [MONITORAMENTO SISTEMA] Sincronização Ativa ---")
    print(f"[{data_hoje} {hora_hoje}] - CPU: {cpu_geral}% | RAM: {ram_pc}%")

    # Carrega o checklist existente para não perder o que já foi guardado
    checklist = {}
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
            try:
                checklist = json.load(f)
            except json.JSONDecodeError:
                checklist = {}

    # Se o ficheiro não existir ou estiver vazio, cria o ciclo de 15 dias a partir de hoje
    if not checklist:
        for i in range(1, 16):
            d = data_hoje + datetime.timedelta(days=i-1)
            checklist[f"Dia {i}"] = {
                "data": str(d),
                "status": "Pendente",
                "ram_app_mb": 0.0,
                "api_ok": False
            }

    # Atualiza o status: Tudo o que for igual ou anterior à data de hoje vira "Concluído"
    for k, v in checklist.items():
        data_item = datetime.date.fromisoformat(v["data"])
        if data_item <= data_hoje:
            v["status"] = "Concluído"
        else:
            v["status"] = "Pendente"

    # Salva o ficheiro atualizado em JSON
    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(checklist, f, indent=4, ensure_ascii=False)

    print(f"\n--- CICLO ATUALIZADO DE 15 DIAS ---")
    for k, v in checklist.items():
        icone = "✅ Concluído" if v["status"] == "Concluído" else "⏳ Pendente"
        destaque = " <--- HOJE" if v["data"] == str(data_hoje) else ""
        print(f"{k} ({v['data']}): {icone}{destaque}")
    print("-" * 50 + "\n")

if __name__ == "__main__":
    executar_monitoramento()