# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - PROPRIETARY TECH DIRECTIVE
===========================================================================
NOTICE: This software source code and its mathematical algorithms are the 
intellectual property of Thierry Technology Concept Global. Unauthorized 
distribution, reverse engineering, or usage without a signed NDA/License 
agreement is strictly prohibited under international copyright frameworks.
===========================================================================
"""

# -*- coding: utf-8 -*-
"""
Módulo de Gerenciamento do Cofre VaultUhnw (Background Worker)
Compliance Mônaco & Auditoria Internacional (Localizado na pasta security)
"""

import os
import re
import time
import json
import shutil
import logging
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from threading import Thread

# Diretório base atual onde este arquivo (vault_manager.py) reside (pasta security)
SECURITY_DIR = Path(__file__).resolve().parent

# Configuração de Logs Estruturados dentro da pasta security
logging.basicConfig(
    filename=str(SECURITY_DIR / 'vault_internal_audit.log'),
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "nivel": "%(levelname)s", "evento": %(message)s}'
)

class VaultUhnw:
    def __init__(self, base_dir: str = "vault_uhnw_storage"):
        """Inicializa a raiz do Cofre Seguro estritamente dentro da pasta security."""
        caminho_passado = Path(base_dir)
        if not caminho_passado.is_absolute():
            self.base_path = (SECURITY_DIR / caminho_passado).resolve()
        else:
            self.base_path = caminho_passado.resolve()
        
        # Definição das pastas dos Cofres de Tempo (Compliance Mônaco)
        self.cofre_15_dias = self.base_path / "COFRE_QUINZENAL"
        self.cofre_1_ano = self.base_path / "COFRE_ANUAL_FISCAL"
        self.cofre_15_anos = self.base_path / "COFRE_HISTORICO_15_ANOS"
        
        # Garante a criação física de toda a estrutura base
        for pasta in [self.base_path, self.cofre_15_dias, self.cofre_1_ano, self.cofre_15_anos]:
            pasta.mkdir(parents=True, exist_ok=True)

    def _sanitizar(self, texto: str) -> str:
        """Limpa textos removendo espaços e caracteres especiais para evitar falhas no SO."""
        if not texto: return "GERAL"
        return re.sub(r'[^a-zA-Z0-9_]', '', texto.upper().strip().replace(" ", "_"))

    def obter_rota_armazenamento(self, nome_empresa: str, nome_ceo: str) -> Path:
        """Cria dinamicamente a pasta organizada do cliente por Nome e Data."""
        empresa_limpa = self._sanitizar(nome_empresa)
        ceo_limpo = self._sanitizar(nome_ceo)
        
        agora = datetime.now()
        ano = agora.strftime("%Y")
        mes_nome = agora.strftime("%m_%B")

        caminho_cliente = self.base_path / empresa_limpa / ceo_limpo / ano / mes_nome
        caminho_cliente.mkdir(parents=True, exist_ok=True)
        return caminho_cliente

    def calcular_assinatura_digital(self, caminho_arquivo: Path) -> str:
        """Gera o hash SHA-256 do arquivo para garantir integridade."""
        sha256_hash = hashlib.sha256()
        try:
            with open(caminho_arquivo, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return "N/A"

    def _arquivo_esta_estavel(self, caminho_arquivo: Path) -> bool:
        """Verifica se o arquivo terminou de ser gravado (evita race condition)."""
        try:
            tamanho_inicial = caminho_arquivo.stat().st_size
            time.sleep(0.5)
            tamanho_final = caminho_arquivo.stat().st_size
            return tamanho_inicial == tamanho_final
        except Exception:
            return False

    def processar_ciclo_de_vida(self, caminho_arquivo: Path, empresa: str):
        """Analisa o arquivo, assina digitalmente e distribui nos cofres."""
        if not caminho_arquivo.is_file() or "COFRE_" in caminho_arquivo.parts:
            return

        if not self._arquivo_esta_estavel(caminho_arquivo):
            return

        agora = datetime.now()
        empresa_limpa = self._sanitizar(empresa)
        hash_documento = self.calcular_assinatura_digital(caminho_arquivo)
        
        data_criacao = datetime.fromtimestamp(caminho_arquivo.stat().st_mtime)
        tempo_de_vida = agora - data_criacao

        # 1. COFRE DE 15 ANOS (Replicação Crônica Imediata)
        destino_15a = self.cofre_15_anos / f"RETENCAO_15A_{empresa_limpa}_{caminho_arquivo.name}"
        if not destino_15a.exists():
            shutil.copy2(caminho_arquivo, destino_15a)
            logging.info(json.dumps({
                "tipo": "REPLICACAO_COMPLIANCE_15A",
                "arquivo": caminho_arquivo.name,
                "assinatura_sha256": hash_documento
            }))

        # 2. COFRE QUINZENAL (Janela Operacional Ativa de 15 dias)
        if tempo_de_vida <= timedelta(days=15):
            pasta_semana = self.cofre_15_dias / agora.strftime("%Y_SEMANA_%V")
            pasta_semana.mkdir(exist_ok=True)
            destino_15d = pasta_semana / caminho_arquivo.name
            if not destino_15d.exists():
                shutil.copy2(caminho_arquivo, destino_15d)

        # 3. COFRE ANUAL (Fechamentos e Auditoria Fiscal de 1 Ano)
        if tempo_de_vida <= timedelta(days=365):
            pasta_balanco = self.cofre_1_ano / agora.strftime("%Y_BALANCO_ANUAL")
            pasta_balanco.mkdir(exist_ok=True)
            destino_1a = pasta_balanco / caminho_arquivo.name
            if not destino_1a.exists():
                shutil.copy2(caminho_arquivo, destino_1a)

    def limpar_cofre_quinzenal_expirado(self):
        """Remove automaticamente arquivos com mais de 15 dias do cofre quinzenal."""
        try:
            agora = datetime.now()
            for arquivo in self.cofre_15_dias.glob("**/*"):
                if arquivo.is_file():
                    idade = agora - datetime.fromtimestamp(arquivo.stat().st_mtime)
                    if idade > timedelta(days=15):
                        arquivo.unlink()
                        logging.info(json.dumps({
                            "tipo": "LIMPEZA_COFRE_QUINZENAL",
                            "arquivo_removido": arquivo.name
                        }))
        except Exception as e:
            logging.error(f"Erro na limpeza do cofre quinzenal: {str(e)}")


def _loop_varredura_preventiva(vault_instance: VaultUhnw):
    """Roda em background alimentando o sistema sozinho."""
    while True:
        try:
            vault_instance.limpar_cofre_quinzenal_expirado()

            for arquivo in list(vault_instance.base_path.glob("**/*")):
                if arquivo.is_file() and not "COFRE_" in arquivo.parts and arquivo.suffix != '.log':
                    rel_path = arquivo.relative_to(vault_instance.base_path)
                    empresa_origem = rel_path.parts[0] if len(rel_path.parts) > 1 else "GERAL"
                    
                    vault_instance.processar_ciclo_de_vida(arquivo, empresa_origem)
        except Exception as e:
            logging.error(f"Falha no motor assíncrono: {str(e)}")
        
        time.sleep(3600)


def ativar_infraestrutura_vault(pasta_raiz: str = "vault_uhnw_storage") -> VaultUhnw:
    """Função mestre que liga o Vault em segundo plano dentro da security."""
    vault = VaultUhnw(pasta_raiz)
    thread_seguranca = Thread(target=_loop_varredura_preventiva, args=(vault,), daemon=True)
    thread_seguranca.start()
    
    logging.info('"Infraestrutura autônoma do Vault ativada com sucesso dentro da pasta security."')
    return vault