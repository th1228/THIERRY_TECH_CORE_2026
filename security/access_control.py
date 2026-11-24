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

# =====================================================================
# ARQUIVO: security/access_control.py
# Controle de Acesso Local Baseado em Papéis (RBAC) - 100% Offline
# =====================================================================

import os
import sys
from typing import Iterable

raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

try:
    from security.log_seguro import LogSeguro
except ImportError:
    from log_seguro import LogSeguro


PERMISSOES_PADRAO: dict[str, set[str]] = {
    "MASTER": {"*"},
    "OPERADOR": {
        "leitura_dados",
        "executar_analise",
        "registrar_auditoria",
        "consultar_cofre",
    },
    "AUDITOR": {
        "leitura_dados",
        "consultar_cofre",
        "verificar_integridade",
        "exportar_relatorio",
    },
    "VISUALIZADOR": {
        "leitura_dados",
    },
}


class AccessControl:
    """
    Gerenciador local de papéis e permissões para operações internas
    do ecossistema sem dependência de rede ou serviços externos.
    """

    def __init__(
        self,
        matriz_permissoes: dict[str, Iterable[str]] | None = None,
        habilitar_log: bool = True,
    ) -> None:
        origem = matriz_permissoes if matriz_permissoes is not None else PERMISSOES_PADRAO
        self._permissoes_por_papel: dict[str, set[str]] = {}
        for papel, acoes in origem.items():
            chave_papel = str(papel).strip().upper()
            self._permissoes_por_papel[chave_papel] = {
                str(acao).strip().lower() for acao in acoes
            }

        self._logger: LogSeguro | None = None
        if habilitar_log:
            try:
                self._logger = LogSeguro()
            except (OSError, RuntimeError):
                self._logger = None

    def _registrar_evento(self, nivel: str, mensagem: str) -> None:
        if self._logger is None:
            return
        try:
            self._logger.registrar("ACCESS_CONTROL", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    def listar_papeis(self) -> list[str]:
        """Retorna os perfis/papéis cadastrados em ordem alfabética."""
        return sorted(self._permissoes_por_papel.keys())

    def permissoes_do_papel(self, papel: str) -> set[str]:
        """Retorna o conjunto de permissões atribuídas ao papel informado."""
        if not isinstance(papel, str) or not papel.strip():
            return set()
        chave = papel.strip().upper()
        return set(self._permissoes_por_papel.get(chave, set()))

    def conceder_permissao(self, papel: str, permissao: str) -> None:
        """Adiciona uma permissão específica a um papel."""
        if not isinstance(papel, str) or not papel.strip():
            raise ValueError("Papel inválido para concessão de permissão.")
        if not isinstance(permissao, str) or not permissao.strip():
            raise ValueError("Permissão inválida para concessão.")

        chave_papel = papel.strip().upper()
        acao_limpa = permissao.strip().lower()
        self._permissoes_por_papel.setdefault(chave_papel, set()).add(acao_limpa)
        self._registrar_evento("INFO", f"Permissão '{acao_limpa}' concedida ao papel '{chave_papel}'.")

    def revogar_permissao(self, papel: str, permissao: str) -> bool:
        """Remove uma permissão de um papel. Retorna True se a permissão existia."""
        if not isinstance(papel, str) or not papel.strip():
            return False
        if not isinstance(permissao, str) or not permissao.strip():
            return False

        chave_papel = papel.strip().upper()
        acao_limpa = permissao.strip().lower()
        acoes = self._permissoes_por_papel.get(chave_papel)
        if not acoes or acao_limpa not in acoes:
            return False

        acoes.remove(acao_limpa)
        self._registrar_evento("ALERTA", f"Permissão '{acao_limpa}' revogada do papel '{chave_papel}'.")
        return True

    def pode_executar(self, papel: str, permissao: str, ator: str = "LOCAL") -> bool:
        """Verifica se o papel possui permissão para executar a ação solicitada."""
        if not isinstance(papel, str) or not papel.strip():
            self._registrar_evento("ALERTA", f"Acesso negado para ator '{ator}': papel vazio ou inválido.")
            return False
        if not isinstance(permissao, str) or not permissao.strip():
            self._registrar_evento("ALERTA", f"Acesso negado para ator '{ator}': permissão vazia ou inválida.")
            return False

        chave_papel = papel.strip().upper()
        acao_limpa = permissao.strip().lower()
        acoes = self._permissoes_por_papel.get(chave_papel, set())

        autorizado = ("*" in acoes) or (acao_limpa in acoes)
        if not autorizado:
            self._registrar_evento(
                "ALERTA",
                f"Acesso negado para ator '{ator}' (papel='{chave_papel}') na ação '{acao_limpa}'.",
            )
        return autorizado

    def exigir_permissao(self, papel: str, permissao: str, ator: str = "LOCAL") -> None:
        """Levanta PermissionError caso o papel não tenha a permissão exigida."""
        if not self.pode_executar(papel=papel, permissao=permissao, ator=ator):
            raise PermissionError(
                f"Acesso negado: papel '{papel}' não possui permissão para '{permissao}'."
            )