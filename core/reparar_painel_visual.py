# -*- coding: utf-8 -*-
"""
Módulo: reparar_painel_visual.py
Descrição: Varre ficheiros HTML e CSS do painel, normalizando z-index >= 100
para 50 (auditoria MIBO) e substituindo termos indesejados no HTML visível
sem alterar blocos <script> ou <style>.
"""

import re
from pathlib import Path

# Ajuste aqui o texto final que você quer no HTML visível
SUBSTITUICOES_HTML = {
    "Tecnologia & Visagismo Trilionário": "Tecnologia & Visagismo / Intangíveis",
    "Visagismo Trilionário": "Visagismo / Intangíveis",
}

PASTAS_IGNORADAS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".idea",
    "build",
    "dist",
    "node_modules",
    "_backup_seguro",
    "_backup_cirurgico",
    "_backup_html_painel",
    "_organizador_aa",
    "backups",
}


def deve_ignorar(caminho: Path) -> bool:
    return any(
        parte.lower() in PASTAS_IGNORADAS or parte.lower().startswith("snap_")
        for parte in caminho.parts
    )


def substituir_no_html_visivel(html: str, antigo: str, novo: str) -> str:
    """Substitui apenas fora de <script> e <style> para não quebrar JS/CSS."""
    protegidos = []

    def guardar_bloco(match):
        protegidos.append(match.group(0))
        return f"__BLOCO_PROTEGIDO_{len(protegidos) - 1}__"

    texto = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        guardar_bloco,
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    texto = texto.replace(antigo, novo)

    for idx, bloco in enumerate(protegidos):
        texto = texto.replace(f"__BLOCO_PROTEGIDO_{idx}__", bloco)

    return texto


def reparar_camadas_painel():
    diretorio_base = Path.cwd()
    print(f"🎨 [SEGURANÇA ATIVA] Verificação profunda de camadas e textos em: {diretorio_base}\n")

    arquivos_alvo = [
        p for p in diretorio_base.rglob("*")
        if p.is_file()
        and p.suffix.lower() in {".html", ".htm", ".css"}
        and not deve_ignorar(p)
    ]

    if not arquivos_alvo:
        print("⚠️ Nenhum ficheiro HTML ou CSS encontrado para varredura.")
        print("\nSTATUS FINAL: NADA ALTERADO.")
        return

    print(f"📁 Total de ficheiros de layout mapeados: {len(arquivos_alvo)}")
    print("=" * 60)

    total_corrigidos = 0
    total_trocas_texto = 0
    erros = []

    for caminho in arquivos_alvo:
        try:
            try:
                conteudo_original = caminho.read_text(encoding="utf-8")
                encoding_usado = "utf-8"
            except UnicodeDecodeError:
                conteudo_original = caminho.read_text(encoding="latin-1")
                encoding_usado = "latin-1"

            def substituir_z_index(match):
                valor_str = match.group(1)
                if not valor_str or not valor_str.isdigit():
                    return match.group(0)
                valor = int(valor_str)
                if valor >= 100:
                    return "z-index: 50"
                return match.group(0)

            conteudo_atualizado = re.sub(
                r"z-index\s*:\s*(\d+)",
                substituir_z_index,
                conteudo_original,
                flags=re.IGNORECASE,
            )

            trocas_neste_arquivo = 0
            if caminho.suffix.lower() in {".html", ".htm"}:
                for antigo, novo in SUBSTITUICOES_HTML.items():
                    antes = conteudo_atualizado.count(antigo)
                    if antes > 0:
                        conteudo_atualizado = substituir_no_html_visivel(
                            conteudo_atualizado, antigo, novo
                        )
                        depois = conteudo_atualizado.count(antigo)
                        feitas = max(0, antes - depois)
                        trocas_neste_arquivo += feitas
                        total_trocas_texto += feitas

            if conteudo_atualizado != conteudo_original:
                backup_path = caminho.with_suffix(caminho.suffix + ".bak")
                if not backup_path.exists():
                    backup_path.write_text(conteudo_original, encoding=encoding_usado)

                caminho.write_text(conteudo_atualizado, encoding=encoding_usado)
                total_corrigidos += 1
                print(
                    f"✔ [CORRIGIDO] {caminho.name} "
                    f"(trocas de texto: {trocas_neste_arquivo} | Backup: {backup_path.name})"
                )
            else:
                print(f"✔ [ESTÁVEL] {caminho.name} sem alterações necessárias.")

        except Exception as e:
            erros.append((caminho.name, str(e)))
            print(f"❌ Erro em {caminho.name}: {e}")

    print("=" * 60)
    print(f"🎯 Varredura concluída! Ficheiros corrigidos nesta ronda: {total_corrigidos}")
    print(f"📝 Substituições de texto feitas no HTML: {total_trocas_texto}\n")

    if erros:
        print(f"STATUS FINAL: DEU PROBLEMA EM {len(erros)} ARQUIVO(S).")
        for nome_arq, msg_erro in erros:
            print(f"  - {nome_arq}: {msg_erro}")
    elif total_corrigidos > 0:
        print("STATUS FINAL: DEU CERTO! Painel atualizado com segurança.")
    else:
        print("STATUS FINAL: DEU CERTO, MAS NADA PRECISOU SER ALTERADO.")


if __name__ == "__main__":
    reparar_camadas_painel()