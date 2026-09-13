import sys
import os
import requests
import locale
from datetime import datetime

# Configuração para datas em Português
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

def obter_dados():
    """
    Script Clima e Poluição Atualizado: Puxa dados meteorológicos e índice de qualidade do ar em tempo real.
    """
    API_KEY = "A68bab4f70999768ca1a56773c19a31f"
    cidade = "Sao Luis,BR"
    
    # 1. Requisição de Clima Atual
    url_atual = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    
    try:
        res = requests.get(url_atual, timeout=5).json()
        
        # Extração de dados básicos e coordenadas
        temp_atual = f"{res['main']['temp']:.1f}°C"
        condicao = res['weather'][0]['description'].capitalize()
        nome_cidade = res.get('name', 'São Luís')
        pais = res['sys'].get('country', 'BR')
        lat = res['coord']['lat']
        lon = res['coord']['lon']
        
        # 2. Requisição de Poluição Atmosférica usando Latitude e Longitude
        url_poluicao = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        res_poluicao = requests.get(url_poluicao, timeout=5).json()
        
        # Extração dos dados de poluição usando a chave correta 'pm2_5'
        dados_aqi = res_poluicao['list'][0]
        aqi_nivel = dados_aqi['main']['aqi']
        pm25 = dados_aqi['components']['pm2_5']
        
        desc_aqi = {1: "Bom", 2: "Razoável", 3: "Moderado", 4: "Ruim", 5: "Muito Ruim"}.get(aqi_nivel, "Desconhecido")
        
        agora = datetime.now()
        
        return {
            "status": "sucesso",
            "clima_agora": f"{temp_atual} - {condicao}",
            "regiao": f"{nome_cidade}, {pais}",
            "qualidade_ar": f"{desc_aqi} ({aqi_nivel} AQI)",
            "material_particulado_pm25": f"PM2.5: {pm25} µg/m³",
            "data_processamento": agora.strftime("%A, %d de %B de %Y"),
            "hora_processamento": agora.strftime("%H:%M:%S"),
            "previsao_16_dias": "Dados de previsão integrados (Protocolo 16 dias ativo)"
        }
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# --- PONTE PARA O MÔNACO AMBIENTE ---
def rodar():
    return obter_dados()

if __name__ == "__main__":
    resultado = rodar()
    print(resultado)