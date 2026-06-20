# -*- coding: utf-8 -*-
import json
import os

class MonacoConsciencia:
    def __init__(self, arquivo_memoria="memoria_historica.json"):
        self.arquivo = arquivo_memoria
        print("[CONSCIÊNCIA] Motor de memória persistente ativado.")

    def consultar_experiencia(self, dados_visuais):
        """Busca o histórico na base de dados."""
        print("[CONSCIÊNCIA] Consultando histórico na base...")
        if not os.path.exists(self.arquivo):
            return None
        
        # Simulação de consulta: aqui você pode adicionar a lógica de busca real
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                memoria = json.load(f)
                return memoria.get("registro_principal")
        except:
            return None

    def aprender_com_sucesso(self, dados, protocolo, nivel):
        """Salva o novo aprendizado na memória."""
        print(f"[CONSCIÊNCIA] Aprendendo novo perfil: {protocolo}...")
        
        novo_registro = {
            "dados": dados,
            "protocolo": protocolo,
            "nivel": nivel
        }
        
        # Salva o aprendizado no arquivo JSON
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump({"registro_principal": novo_registro}, f, indent=4, ensure_ascii=False)
            
        print("[CONSCIÊNCIA] Perfil armazenado com sucesso na memória.")
        return True