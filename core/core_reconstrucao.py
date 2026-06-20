# -*- coding: utf-8 -*-
import biometria
import diagnostico_ante_gravidade_neural
import neuro_gravidade_preditor

def executar_reconstrucao_total():
    """
    Este motor coleta todos os resultados, consolida num único 
    dicionário e retorna para quem chamou (o Gerador de Relatório).
    """
    
    # Coletamos os dados de cada engine (certifique-se que elas tenham 
    # funções chamadas 'obter_dados' que retornam um dicionário)
    try:
        dados_consolidado = {
            "biometria": biometria.obter_dados(),
            "diagnostico": diagnostico_ante_gravidade_neural.obter_dados(),
            "neuro": neuro_gravidade_preditor.obter_dados(),
            "status_orquestracao": "Processamento concluído com sucesso"
        }
        return dados_consolidado
    except Exception as e:
        return {"erro": str(e)}

# NOTA IMPORTANTE: 
# Remova qualquer print ou subprocess.Popen deste arquivo.
# Ele agora serve apenas para fornecer dados.