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
# ARQUIVO: security/security_orchestrator.py
# Orquestrador Local de Camadas de Segurança (100% Offline)
# =====================================================================

import os
import sys
from pathlib import Path
from typing import Any

SECURITY_DIR = Path(__file__).resolve().parent
RAIZ_PROJETO = SECURITY_DIR.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.append(str(RAIZ_PROJETO))

try:
    from security.audit_reporter import AuditReporter
    from security.config_guard import ConfigGuard
    from security.integrity_guard import IntegrityGuard
    from security.log_seguro import LogSeguro
    from security.sandbox_guard import SandboxGuard
    from security.secret_scanner import SecretScanner
except ImportError:
    from audit_reporter import AuditReporter
    from config_guard import ConfigGuard
    from integrity_guard import IntegrityGuard
    from log_seguro import LogSeguro
    from sandbox_guard import SandboxGuard
    from secret_scanner import SecretScanner


class SecurityOrchestrator:
    """
    Coordena verificações locais de integridade, configuração, varredura de
    segredos, isolamento de caminho e emissão de relatórios em ambiente 100% offline.
    """

    def __init__(self, habilitar_log: bool = True) -> None:
        self.integrity = IntegrityGuard()
        self.config = ConfigGuard(habilitar_log=False)
        self.scanner = SecretScanner(habilitar_log=False)
        self.sandbox = SandboxGuard(habilitar_log=False)
        self.reporter = AuditReporter(habilitar_log=False)
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
            self._logger.registrar("SECURITY_ORCHESTRATOR", nivel, mensagem)
        except (OSError, RuntimeError):
            pass

    def validar_caminho_seguro(
        self,
        caminho: str | os.PathLike[str],
        base_relativa: str | os.PathLike[str] | None = None,
    ) -> Path:
        """Valida e resolve um caminho dentro da sandbox permitida."""
        return self.sandbox.resolver_caminho_seguro(caminho, base_relativa=base_relativa)

    def executar_diagnostico(
        self,
        arquivos_para_escanear: list[str | os.PathLike[str]] | None = None,
        config_dict: dict[str, Any] | None = None,
        salvar_relatorio: bool = False,
        nome_relatorio: str = "diagnostico_security",
    ) -> dict[str, Any]:
        """
        Executa uma rodada de checagens locais e retorna um relatório consolidado
        com score de 0 a 100.
        """
        verificacoes: list[dict[str, Any]] = []
        alertas: list[str] = []
        peso_total = 0.0
        peso_aprovado = 0.0

        # 1. Estado de bloqueio operacional (system.lock)
        peso_total += 25.0
        bloqueado = self.integrity.esta_bloqueado()
        if bloqueado:
            msg = "Trava operacional (system.lock) está ativa."
            verificacoes.append({"modulo": "IntegrityGuard", "status": "ALERTA", "detalhe": msg})
            alertas.append(msg)
        else:
            peso_aprovado += 25.0
            verificacoes.append(
                {"modulo": "IntegrityGuard", "status": "OK", "detalhe": "Sem trava de bloqueio ativa."}
            )

        # 2. Manifesto de integridade (se existir)
        peso_total += 25.0
        if self.integrity.manifest_path.is_file():
            ok_manifesto, divergencias = self.integrity.verificar_manifesto()
            if ok_manifesto:
                peso_aprovado += 25.0
                verificacoes.append(
                    {"modulo": "IntegrityManifest", "status": "OK", "detalhe": "Manifesto íntegro."}
                )
            else:
                verificacoes.append(
                    {
                        "modulo": "IntegrityManifest",
                        "status": "ALERTA",
                        "detalhe": f"{len(divergencias)} divergência(s) detectada(s).",
                    }
                )
                alertas.extend(divergencias)
        else:
            peso_aprovado += 25.0
            verificacoes.append(
                {
                    "modulo": "IntegrityManifest",
                    "status": "OK",
                    "detalhe": "Nenhum manifesto gerado ainda (sem divergências).",
                }
            )

        # 3. Auditoria de configuração (se fornecida)
        if config_dict is not None:
            peso_total += 25.0
            try:
                segredos_cfg = self.config.auditar_segredos_em_config(config_dict)
                if not segredos_cfg:
                    peso_aprovado += 25.0
                    verificacoes.append(
                        {
                            "modulo": "ConfigGuard",
                            "status": "OK",
                            "detalhe": "Sem segredos literais em configuração.",
                        }
                    )
                else:
                    msg = f"Segredos literais em configuração: {', '.join(segredos_cfg)}."
                    verificacoes.append({"modulo": "ConfigGuard", "status": "ALERTA", "detalhe": msg})
                    alertas.append(msg)
            except (TypeError, ValueError) as e:
                msg = f"Falha na auditoria de configuração: {e}"
                verificacoes.append({"modulo": "ConfigGuard", "status": "ERRO", "detalhe": msg})
                alertas.append(msg)

        # 4. Varredura de segredos em arquivos indicados
        if arquivos_para_escanear:
            peso_total += 25.0
            total_achados = 0
            for item in arquivos_para_escanear:
                try:
                    achados = self.scanner.escanear_arquivo(item)
                    total_achados += len(achados)
                    for achado in achados:
                        alertas.append(
                            f"{achado['origem']}:{achado['linha']} -> {achado['regra']} ({achado['amostra']})"
                        )
                except (FileNotFoundError, OSError, ValueError) as e:
                    alertas.append(f"Falha ao escanear '{item}': {e}")

            if total_achados == 0 and not any("Falha ao escanear" in a for a in alertas):
                peso_aprovado += 25.0
                verificacoes.append(
                    {
                        "modulo": "SecretScanner",
                        "status": "OK",
                        "detalhe": f"{len(arquivos_para_escanear)} arquivo(s) escaneado(s) sem indícios.",
                    }
                )
            else:
                verificacoes.append(
                    {
                        "modulo": "SecretScanner",
                        "status": "ALERTA",
                        "detalhe": f"{total_achados} indício(s) encontrado(s).",
                    }
                )

        score = (peso_aprovado / peso_total * 100.0) if peso_total > 0 else 100.0
        relatorio = self.reporter.construir_relatorio(
            titulo="Diagnóstico Local de Segurança - TTC Global",
            score_conformidade=score,
            verificacoes=verificacoes,
            alertas=alertas,
        )

        if salvar_relatorio:
            try:
                self.reporter.salvar_relatorio(relatorio, nome_base=nome_relatorio)
            except (OSError, RuntimeError, TypeError, ValueError) as e:
                self._registrar("ALERTA", f"Não foi possível persistir relatório: {e}")

        self._registrar(
            "INFO",
            f"Diagnóstico concluído (score={relatorio['score_conformidade']}, status={relatorio['status_global']}).",
        )
        return relatorio