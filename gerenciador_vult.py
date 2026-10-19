# -*- coding: utf-8 -*-
"""
Módulo: gerenciador_vault.py
Sistema: Thierry Technology Concept Global - Sovereign C2 Defense Engine
Descrição: Gerenciador de Vault UHNW para armazenamento seguro e estruturado
           de relatórios e dossiês de salvaguarda patrimonial.
"""

import os
from typing import Optional


class GerenciadorVaultUHNW:
    """
    Classe responsável por gerenciar o Vault de segurança, definindo diretórios
    criptografados/organizados para a salvaguarda de documentos e PDFs gerados.
    """

    def __init__(self, raiz_vault: Optional[str] = None) -> None:
        if raiz_vault:
            self.raiz_vault = os.path.abspath(raiz_vault)
        else:
            # Define o diretório padrão do Vault na raiz do projeto ou diretório do usuário
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.raiz_vault = os.path.join(current_dir, "vault_uhnw_storage")
            
        os.makedirs(self.raiz_vault, exist_ok=True)

    def preparar_destino_arquivo(self, nome_cliente: str, tipo_relatorio: str = "temp", extensao: str = "pdf") -> str:
        """
        Prepara e retorna o caminho absoluto seguro para salvar o arquivo do cliente,
        criando subdiretórios categorizados conforme necessário.
        """
        nome_limpo = "".join(c if c.isalnum() else "_" for c in nome_cliente).upper()
        
        # Subdiretório por categoria de relatório ou cliente
        pasta_destino = os.path.join(self.raiz_vault, "dossies_finais", nome_limpo)
        os.makedirs(pasta_destino, exist_ok=True)
        
        nome_arquivo = f"RELATORIO_{tipo_relatorio.upper()}_{nome_limpo}.{extensao.lstrip('.')}"
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        
        return caminho_completo

    def verificar_integridade_vault(self) -> bool:
        """
        Verifica se o diretório do Vault está acessível e operacional.
        """
        try:
            return os.path.exists(self.raiz_vault) and os.access(self.raiz_vault, os.W_OK)
        except OSError:
            return False
