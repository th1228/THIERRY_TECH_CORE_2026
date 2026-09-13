# =====================================================================
# ARQUIVO: security/input_sanitizer.py
# =====================================================================

import re

class InputSanitizer:
    """
    Classe responsável por higienizar entradas de texto, neutralizando 
    tentativas de injeção de código (SQL Injection e XSS).
    """

    @staticmethod
    def limpar_string(texto: str) -> str:
        """
        Remove símbolos perigosos, espaços e caracteres especiais,
        permitindo apenas letras, números e underscores (_).
        Elimina completamente traços (--), ponto e vírgula (;) e aspas.
        """
        if not isinstance(texto, str):
            return ""
        
        # Regex restritiva: remove tudo o que não for alfanumérico ou underscore
        texto_limpo = re.sub(r'[^a-zA-Z0-9_]', '', texto)
        return texto_limpo

    @staticmethod
    def limpar_dicionario(dados: dict) -> dict:
        """
        Percorre um dicionário inteiro e limpa todas as strings contidas nele,
        garantindo que nenhum payload malicioso passe adiante.
        """
        dados_limpos = {}
        for chave, valor in dados.items():
            if isinstance(valor, str):
                dados_limpos[chave] = InputSanitizer.limpar_string(valor)
            elif isinstance(valor, dict):
                dados_limpos[chave] = InputSanitizer.limpar_dicionario(valor)
            else:
                dados_limpos[chave] = valor
        return dados_limpos