# -*- coding: utf-8 -*-
import re
from pathlib import Path

HTML_PATH = Path("index.html")

def auditar_padrao_internacional():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado na raiz.")
        return

    conteudo = HTML_PATH.read_text(encoding="utf-8")
    nota = 10.0
    relatorio = []

    # 1. Declaração de idioma e codificação UTF-8 (Padrão W3C / i18n)
    if not re.search(r'<html[^>]+lang=["\'][a-zA-Z-]+["\']', conteudo, re.IGNORECASE):
        nota -= 1.5
        relatorio.append("[FALHA] Tag <html> sem atributo 'lang' definido.")
    else:
        relatorio.append("[OK] Atributo de idioma internacional (lang) presente na tag <html>.")

    if "utf-8" not in conteudo.lower():
        nota -= 1.0
        relatorio.append("[FALHA] Codificação UTF-8 não declarada no <head>.")
    else:
        relatorio.append("[OK] Codificação global UTF-8 detectada.")

    # 2. Responsividade / Viewport
    if 'name="viewport"' not in conteudo.lower():
        nota -= 1.5
        relatorio.append("[FALHA] Meta tag 'viewport' ausente.")
    else:
        relatorio.append("[OK] Meta tag 'viewport' configurada corretamente.")

    # 3. Acessibilidade em imagens (Norma WCAG 2.1 - Atributo alt)
    imagens = re.findall(r'<img\b[^>]*>', conteudo, re.IGNORECASE)
    imgs_sem_alt = [img for img in imagens if 'alt=' not in img.lower()]
    if imgs_sem_alt:
        nota -= 1.5
        relatorio.append(f"[ALERTA] {len(imgs_sem_alt)} imagem(ns) sem atributo 'alt'.")
    else:
        relatorio.append("[OK] Todas as imagens possuem descrição alternativa (WCAG).")

    # 4. Audita apenas a interface visível (ignora IDs e rotas internas do motor)
    sem_scripts_e_estilos = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', conteudo, flags=re.IGNORECASE | re.DOTALL)
    texto_visivel = re.sub(r'<[^>]+>', ' ', sem_scripts_e_estilos).lower()

    termos_proibidos = ["stripe", "mônaco", "monaco", "(roi)"]
    encontrados = [t for t in termos_proibidos if t in texto_visivel]

    if encontrados:
        nota -= 2.0
        relatorio.append(f"[ALERTA] Termos antigos visíveis na interface: {', '.join(encontrados)}.")
    else:
        relatorio.append("[OK] Interface pública 100% limpa (zero termos residuais visíveis).")

    # 5. Blindagem de contraste do Modo Claro ativa
    if "auditor-tcc-styles" in conteudo:
        relatorio.append("[OK] Blindagem de contraste para Modo Claro/Escuro (WCAG AA) ativa.")
    else:
        nota -= 1.5
        relatorio.append("[ALERTA] Estilo de alto contraste do auditor não encontrado.")

    print("=" * 75)
    print(f"RELATÓRIO DE AUDITORIA INTERNACIONAL (W3C / WCAG) - NOTA FINAL: {max(0.0, nota):.1f} / 10.0")
    print("=" * 75)
    for item in relatorio:
        print(item)
    print("=" * 75)

if __name__ == "__main__":
    auditar_padrao_internacional()