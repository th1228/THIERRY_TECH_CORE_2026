import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -*- coding: utf-8 -*-
"""
Script: teste_seguro_zerados.py
Finalidade: Verifica integridade e execução do sistema antes de apagar arquivos
            zerados (0 bytes), cria cópia de recuperação, pede confirmação,
            apaga, retesta o programa, e oferece função de recomposição/resgate
            caso ocorra erro ou impedimento de execução.
"""

import os
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime
from typing import List, Optional, Set, Tuple

PASTAS_IGNORADAS: Set[str] = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "pdfs_finais",
    "_reserva_segura",
    "_cofre_recuperacao_zerados",
}

ALVOS_PADRAO: List[str] = [
    "Documentos/th.prn",
    "STORAGE_DATA/thierry_tech_biogenio.db",
    "security/core/ultimo_motodiagnostico.json",
    "tools/vault_internal_audit.log",
]


def _normalizar_rel(rel: str) -> str:
    return rel.replace("\\", "/").strip()


def _caminho_absoluto(raiz: str, rel: str) -> str:
    return os.path.join(raiz, _normalizar_rel(rel).replace("/", os.sep))


def _criar_cofre_recuperacao(raiz: str, alvos: List[str]) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cofre = os.path.join(raiz, "_cofre_recuperacao_zerados", f"snapshot_{stamp}")
    os.makedirs(cofre, exist_ok=True)

    manifesto = os.path.join(cofre, "manifesto_alvos.txt")
    with open(manifesto, "w", encoding="utf-8") as f:
        for rel in alvos:
            rel_norm = _normalizar_rel(rel)
            origem = _caminho_absoluto(raiz, rel_norm)
            existe = os.path.isfile(origem)
            tam = os.path.getsize(origem) if existe else -1
            f.write(f"{rel_norm}|existe={existe}|tamanho={tam}\n")
            if existe:
                destino = os.path.join(cofre, "arquivos", rel_norm.replace("/", os.sep))
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                shutil.copy2(origem, destino)

    return cofre


def _ultimo_cofre(raiz: str) -> Optional[str]:
    base = os.path.join(raiz, "_cofre_recuperacao_zerados")
    if not os.path.isdir(base):
        return None
    pastas = sorted(
        [
            os.path.join(base, d)
            for d in os.listdir(base)
            if os.path.isdir(os.path.join(base, d))
        ]
    )
    return pastas[-1] if pastas else None


def verificar_integridade_e_sistema(raiz: str) -> Tuple[bool, str]:
    """Verifica compilação dos .py e testa execução básica do sistema."""
    erros: List[str] = []

    main_py = os.path.join(raiz, "main.py")
    if not os.path.isfile(main_py):
        return False, "Arquivo principal 'main.py' não encontrado."

    candidatos_compilacao: List[str] = [main_py]
    for subpasta in ("core", "legal", "security", "tools"):
        pasta_abs = os.path.join(raiz, subpasta)
        if os.path.isdir(pasta_abs):
            for atual, dirs, arquivos in os.walk(pasta_abs):
                dirs[:] = [d for d in sorted(dirs) if d not in PASTAS_IGNORADAS]
                for nome in sorted(arquivos):
                    if nome.endswith(".py"):
                        candidatos_compilacao.append(os.path.join(atual, nome))

    for arq in candidatos_compilacao:
        try:
            py_compile.compile(arq, doraise=True)
        except py_compile.PyCompileError as exc:
            erros.append(f"Falha de sintaxe/compilação em {os.path.relpath(arq, raiz)}: {exc}")

    codigo_sonda = (
        "import importlib.util, sys\n"
        f"spec = importlib.util.spec_from_file_location('main_probe', r'{main_py}')\n"
        "if spec is None or spec.loader is None:\n"
        "    raise RuntimeError('Não foi possível carregar main.py')\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        "logger.info('SONDA_OK')\n"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", codigo_sonda],
            cwd=raiz,
            capture_output=True,
            text=True,
            timeout=25,
        )
        if proc.returncode != 0 or "SONDA_OK" not in proc.stdout:
            detalhe = (proc.stderr or proc.stdout or "Erro desconhecido ao rodar main.py").strip()
            erros.append(f"Programa impedido de rodar: {detalhe}")
    except subprocess.TimeoutExpired:
        erros.append("Tempo esgotado (timeout) ao testar execução de main.py.")
    except Exception as exc:
        erros.append(f"Erro ao executar sonda do sistema: {exc}")

    if erros:
        return False, " | ".join(erros)
    return True, "Sistema íntegro e 100% ativo na verificação."


def apagar_arquivos_alvo(raiz: str, alvos: List[str]) -> Tuple[List[str], List[str]]:
    apagados: List[str] = []
    falhas: List[str] = []
    for rel in alvos:
        rel_norm = _normalizar_rel(rel)
        caminho = _caminho_absoluto(raiz, rel_norm)
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
                apagados.append(rel_norm)
            except Exception as exc:
                falhas.append(f"{rel_norm}: {exc}")
    return apagados, falhas


def recompor_arquivos_zerados(
    raiz: str, alvos: List[str], caminho_cofre: Optional[str] = None
) -> Tuple[bool, str]:
    """Devolve os arquivos do cofre (ou recria vazios se não houver no cofre)."""
    cofre = caminho_cofre or _ultimo_cofre(raiz)
    erros: List[str] = []
    restaurados: List[str] = []

    for rel in alvos:
        rel_norm = _normalizar_rel(rel)
        destino = _caminho_absoluto(raiz, rel_norm)
        try:
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            origem_cofre = (
                os.path.join(cofre, "arquivos", rel_norm.replace("/", os.sep))
                if cofre
                else ""
            )
            if origem_cofre and os.path.isfile(origem_cofre):
                shutil.copy2(origem_cofre, destino)
            else:
                with open(destino, "w", encoding="utf-8"):
                    pass
            restaurados.append(rel_norm)
        except Exception as exc:
            erros.append(f"{rel_norm}: {exc}")

    if erros:
        return False, "Erro ao recompor arquivos: " + " | ".join(erros)

    ok_pos, msg_pos = verificar_integridade_e_sistema(raiz)
    if not ok_pos:
        return False, f"Arquivos recompostos ({len(restaurados)}), mas o sistema ainda acusa erro: {msg_pos}"

    return True, f"Arquivos recompostos com sucesso ({len(restaurados)}) e sistema voltou a rodar 100%."


def loop_resgate_se_necessario(raiz: str, alvos: List[str], cofre: str) -> None:
    while True:
        resp = input("\nDeseja resgatar / recompor os arquivos de volta agora? (sim/nao): ").strip().lower()
        if resp not in {"sim", "s", "yes", "y"}:
            logger.info("Resgate não executado nesta etapa.")
            return

        ok_rec, msg_rec = recompor_arquivos_zerados(raiz, alvos, cofre)
        if ok_rec:
            logger.info(f"[OK] {msg_rec}")
            return

        logger.info(f"[ERRO] {msg_rec}")
        logger.info("Execute a nova função de recomposição novamente para tentar trazer os arquivos de volta.")


def executar_fluxo() -> None:
    raiz = os.path.abspath(os.path.dirname(__file__))
    alvos = [a for a in ALVOS_PADRAO if os.path.exists(_caminho_absoluto(raiz, a))]

    if not alvos:
        alvos = ALVOS_PADRAO

    logger.info("=" * 72)
    logger.info("1. VERIFICANDO INTEGRIDADE E EXECUÇÃO DO SISTEMA (100%)")
    logger.info("=" * 72)
    ok_antes, parecer_antes = verificar_integridade_e_sistema(raiz)
    logger.info(f"Parecer inicial: {parecer_antes}")
    if ok_antes:
        logger.info("Status: SIM — O sistema está rodando 100% com os arquivos atuais.")
    else:
        logger.info("Status: ATENÇÃO — Há erro/impedimento detectado antes da remoção.")

    cofre = _criar_cofre_recuperacao(raiz, alvos)
    logger.info(f"[OK] Cópia de segurança criada em: {cofre}")

    logger.info("\nArquivos alvo:")
    for item in alvos:
        logger.info(f"  - {item}")

    escolha = input("\nVocê quer apagar esses arquivos com segurança agora? (sim/nao): ").strip().lower()
    if escolha not in {"sim", "s", "yes", "y"}:
        logger.info("Operação cancelada. Nenhum arquivo foi apagado.")
        return

    apagados, falhas = apagar_arquivos_alvo(raiz, alvos)
    logger.info(f"[OK] Apagados ({len(apagados)}): {', '.join(apagados) if apagados else 'nenhum'}")
    if falhas:
        logger.info(f"[ERRO] Falhas ao apagar: {' | '.join(falhas)}")

    logger.info("\n" + "=" * 72)
    logger.info("2. TESTANDO O PROGRAMA NOVAMENTE APÓS APAGAR")
    logger.info("=" * 72)
    ok_depois, parecer_depois = verificar_integridade_e_sistema(raiz)
    if ok_depois:
        logger.info(f"[OK] Programa continua rodando 100% ativo sem os arquivos. ({parecer_depois})")
        return

    logger.info(f"[ERRO] Programa impedido de rodar ou deu erro: {parecer_depois}")
    logger.info("Execute a função recompor_arquivos_zerados() para devolver os arquivos vazios de volta.")
    loop_resgate_se_necessario(raiz, alvos, cofre)


if __name__ == "__main__":
    executar_fluxo()