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
# ARQUIVO: security/audit_reporter.py
# Gerador Local de Relatórios de Auditoria e Conformidade (100% Offline)
# =====================================================================

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECURITY_DIR = Path(__file__).resolve().parent
RAIZ_PROJETO = SECURITY_DIR.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.append(str(RAIZ_PROJETO))

try:
    from security.log_seguro import LogSeguro
except ImportError:
    from log_seguro import LogSeguro

DEFAULT_REPORT_DIR = SECURITY_DIR / "reports"


class AuditReporter:
    """
    Consolida métricas e achados de auditoria local em estruturas padronizadas,
    texto Markdown e arquivos salvos em disco sem dependência de rede.
    """

    def __init__(
        self,
        report_dir: str | os.PathLike[str] | None = None,
        habilitar_log: bool = True,
    ) -> None:
        self.report_dir = Path(report_dir) if report_dir else DEFAULT_REPORT_DIR
        self._logger: LogSeguro | None = self._iniciar_logger() if habilitar_log else None

    @staticmethod
    def _iniciar_logger() -> LogSeguro | None:
        try:
            return LogSeguro()
        except (OSError, RuntimeError):
            return None

    def _registrar(self, nivel: str, mensagem: str) -> None:
        if self._logger is None:
            return
        try:
            self._logger.registrar("AUDIT_REPORTER", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    @staticmethod
    def _normalizar_score(score: float | int) -> float:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("O score de conformidade deve ser numérico.")
        valor = float(score)
        if valor < 0.0:
            return 0.0
        if valor > 100.0:
            return 100.0
        return round(valor, 2)

    def construir_relatorio(
        self,
        titulo: str,
        score_conformidade: float | int,
        verificacoes: list[dict[str, Any]],
        alertas: list[str] | None = None,
    ) -> dict[str, Any]:
        """Monta um relatório estruturado de auditoria com score normalizado (0 a 100)."""
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("O título do relatório não pode ser vazio.")
        if not isinstance(verificacoes, list):
            raise TypeError("As verificações devem ser fornecidas em uma lista de dicionários.")

        score_limpo = self._normalizar_score(score_conformidade)
        lista_alertas = [str(item) for item in (alertas or []) if str(item).strip()]

        itens_normalizados: list[dict[str, Any]] = []
        for item in verificacoes:
            if not isinstance(item, dict):
                raise TypeError("Cada item em 'verificacoes' deve ser um dicionário.")
            itens_normalizados.append(
                {
                    "modulo": str(item.get("modulo", "GERAL")),
                    "status": str(item.get("status", "OK")).upper(),
                    "detalhe": str(item.get("detalhe", "")),
                }
            )

        status_global = "CONFORME" if score_limpo >= 100.0 and not lista_alertas else "ATENCAO"
        return {
            "titulo": titulo.strip(),
            "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
            "score_conformidade": score_limpo,
            "status_global": status_global,
            "total_verificacoes": len(itens_normalizados),
            "total_alertas": len(lista_alertas),
            "verificacoes": itens_normalizados,
            "alertas": lista_alertas,
        }

    def renderizar_markdown(self, relatorio: dict[str, Any]) -> str:
        """Converte um relatório estruturado em texto Markdown legível para auditoria."""
        if not isinstance(relatorio, dict):
            raise TypeError("O relatório deve ser um dicionário.")

        linhas: list[str] = [
            f"# {relatorio.get('titulo', 'Relatório de Auditoria')}",
            "",
            f"- **Gerado em (UTC):** {relatorio.get('gerado_em_utc', '')}",
            f"- **Score de Conformidade:** {relatorio.get('score_conformidade', 0)} / 100",
            f"- **Status Global:** {relatorio.get('status_global', 'ATENCAO')}",
            f"- **Total de Verificações:** {relatorio.get('total_verificacoes', 0)}",
            f"- **Total de Alertas:** {relatorio.get('total_alertas', 0)}",
            "",
            "## Verificações",
        ]

        verificacoes = relatorio.get("verificacoes", [])
        if isinstance(verificacoes, list) and verificacoes:
            for item in verificacoes:
                if isinstance(item, dict):
                    modulo = item.get("modulo", "GERAL")
                    status = item.get("status", "OK")
                    detalhe = item.get("detalhe", "")
                    linhas.append(f"- **{modulo}** [{status}]: {detalhe}")
        else:
            linhas.append("- Nenhuma verificação registrada.")

        alertas = relatorio.get("alertas", [])
        linhas.extend(["", "## Alertas"])
        if isinstance(alertas, list) and alertas:
            for alerta in alertas:
                linhas.append(f"- {alerta}")
        else:
            linhas.append("- Nenhum alerta pendente.")

        return "\n".join(linhas) + "\n"

    def salvar_relatorio(
        self,
        relatorio: dict[str, Any],
        nome_base: str = "auditoria_security",
    ) -> tuple[Path, Path]:
        """
        Salva o relatório em formato JSON e Markdown no diretório de relatórios.
        Retorna (caminho_json, caminho_md).
        """
        if not isinstance(relatorio, dict):
            raise TypeError("O relatório deve ser um dicionário.")
        if not isinstance(nome_base, str) or not nome_base.strip():
            raise ValueError("O nome base do relatório não pode ser vazio.")

        nome_limpo = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in nome_base.strip())
        caminho_json = self.report_dir / f"{nome_limpo}.json"
        caminho_md = self.report_dir / f"{nome_limpo}.md"

        conteudo_md = self.renderizar_markdown(relatorio)

        try:
            self.report_dir.mkdir(parents=True, exist_ok=True)
            with caminho_json.open("w", encoding="utf-8") as f_json:
                json.dump(relatorio, f_json, indent=2, ensure_ascii=False, sort_keys=True)
            with caminho_md.open("w", encoding="utf-8") as f_md:
                f_md.write(conteudo_md)
        except OSError as e:
            self._registrar("ERRO", f"Falha ao salvar relatório '{nome_limpo}': {e}")
            raise RuntimeError(f"Não foi possível gravar os arquivos de relatório: {e}") from e

        self._registrar(
            "INFO",
            f"Relatório '{nome_limpo}' salvo (score={relatorio.get('score_conformidade')}).",
        )
        return caminho_json, caminho_md