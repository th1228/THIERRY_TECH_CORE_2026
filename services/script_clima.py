import requests
from datetime import datetime, timedelta

# 1. Suas 10 cidades globais com as coordenadas geográficas aproximadas
# (A API Open-Meteo trabalha diretamente com Latitude e Longitude para precisão global)
cidades_coordenadas = {
    "Manhattan": {"lat": 40.7834, "lon": -73.9662},
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "Tóquio": {"lat": 35.6762, "lon": 139.6503},
    "Cingapura": {"lat": 1.3521, "lon": 103.8198},
    "Mônaco": {"lat": 43.7384, "lon": 7.4246},
    "Dubai": {"lat": 25.2048, "lon": 55.2708},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Berlim": {"lat": 52.5200, "lon": 13.4050},
    "Suíça": {"lat": 46.8182, "lon": 8.2275} # Centralizado em Zurique/região central
}

def buscar_previsao_16_dias(cidade, lat, lon):
    """
    Consome a API gratuita Open-Meteo para buscar a previsão dos próximos 16 dias.
    """
    # URL base da API pública (repare o parâmetro forecast_days=16)
    url = "https://api.open-meteo.com/v1/forecast"
    
    parametros = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 16
    }
    
    try:
        resposta = requests.get(url, params=parametros)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get("daily", {})
        else:
            print(f"Erro ao acessar dados para {cidade}: Status {resposta.status_code}")
            return None
    except Exception as e:
        print(f"Falha na conexão ao buscar {cidade}: {e}")
        return None

# 2. Execução do loop de consulta para toda a sua estrutura de cidades
print("=== CONSULTANDO PREVISÃO DE 16 DIAS (API GRATUITA) ===")

for cidade, coords in cidades_coordenadas.items():
    print(f"\nBuscando dados para: {cidade}...")
    previsao = buscar_previsao_16_dias(cidade, coords["lat"], coords["lon"])
    
    if previsao:
        # Exibe apenas os primeiros dias no console como demonstração da estrutura
        datas = previsao.get("time", [])
        temp_max = previsao.get("temperature_2m_max", [])
        temp_min = previsao.get("temperature_2m_min", [])
        chuva_prob = previsao.get("precipitation_probability_max", [])
        
        print(f"-> Sucesso! Retornados {len(datas)} dias de previsão.")
        print(f"   Exemplo do Dia 1 ({datas[0]}): Mín: {temp_min[0]}°C | Máx: {temp_max[0]}°C | Chance de Chuva: {chuva_prob[0]}%")
        
        # Aqui você pode salvar no seu banco de dados ou usar na sua interface:
        # Ex: salvar_no_banco(cidade, previsao) 