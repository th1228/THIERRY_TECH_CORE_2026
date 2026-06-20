# -*- coding: utf-8 -*-
import datetime

# Dicionário Mestre de Elite
laudo_acumulado = {
    "cliente": {},
    "bio_identidade": {},
    "capilar": {},
    "monaco_plan": {},
    "contexto_ambiental": {} # O clima agora é parte integrante do seu laudo
}

def obter_clima_atualizado():
    """
    Busca o contexto ambiental de São Luís. 
    Nota: Em um sistema de produção, você plugará aqui uma API real (ex: OpenWeather).
    """
    # Exemplo com dados fixos para garantir funcionamento imediato
    return {
        "local": "São Luís, MA",
        "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "temperatura": "29°C",
        "condicao": "Nublado",
        "umidade": "85%"
    }

def salvar_dados(categoria, novos_dados):
    """Salva os dados coletados pela câmera ou sistemas de análise."""
    if categoria in laudo_acumulado:
        laudo_acumulado[categoria].update(novos_dados)
        print(f"Sucesso: Dados de '{categoria}' integrados com sucesso.")
    else:
        print(f"Erro: Categoria '{categoria}' desconhecida.")

def inicializar_sistema():
    """Carrega o contexto inicial (Clima) ao iniciar o software."""
    clima = obter_clima_atualizado()
    salvar_dados("contexto_ambiental", clima)
    print("Sistema TTC Global inicializado com contexto ambiental.")

def obter_laudo_completo():
    """Retorna tudo o que foi acumulado para ser impresso no PDF."""
    return laudo_acumulado

# Inicializa o clima assim que o módulo for importado
inicializar_sistema()