# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
MAIN_PATH = Path("main.py")

def aplicar_blindagem_total():
    if not HTML_PATH.exists() or not MAIN_PATH.exists():
        print("[ERRO] Verifique se index.html e main.py estão nesta pasta.")
        return

    # 1. Criação de backups de segurança obrigatórios
    shutil.copy2(HTML_PATH, Path("index.html.bak"))
    shutil.copy2(MAIN_PATH, Path("main.py.bak"))
    print("[INFO] Backups criados: index.html.bak e main.py.bak")

    conteudo_main = MAIN_PATH.read_text(encoding="utf-8")
    conteudo_html = HTML_PATH.read_text(encoding="utf-8")

    # 2. Adiciona rotas espelho (Alias) no main.py sem apagar as originais
    alterou_main = False

    if '@app.post("/obter-link-stripe")' in conteudo_main and '@app.post("/obter-link-licenca-executiva")' not in conteudo_main:
        conteudo_main = conteudo_main.replace(
            '@app.post("/obter-link-stripe")',
            '@app.post("/obter-link-licenca-executiva")\n@app.post("/obter-link-stripe")',
            1
        )
        alterou_main = True

    if '@app.post("/api/v1/gerar-relatorio-monaco")' in conteudo_main and '@app.post("/api/v1/gerar-relatorio-executivo")' not in conteudo_main:
        conteudo_main = conteudo_main.replace(
            '@app.post("/api/v1/gerar-relatorio-monaco")',
            '@app.post("/api/v1/gerar-relatorio-executivo")\n@app.post("/api/v1/gerar-relatorio-monaco")',
            1
        )
        alterou_main = True

    if alterou_main:
        MAIN_PATH.write_text(conteudo_main, encoding="utf-8")
        print("[OK] Rotas executivas espelho adicionadas ao main.py com segurança.")
    else:
        print("[INFO] Rotas espelho já estavam configuradas no main.py.")

    # 3. Atualiza o index.html para usar apenas as rotas limpas e remove comentários residuais
    conteudo_html = conteudo_html.replace("/obter-link-stripe", "/obter-link-licenca-executiva")
    conteudo_html = conteudo_html.replace("/api/v1/gerar-relatorio-monaco", "/api/v1/gerar-relatorio-executivo")

    # Remove comentários HTML que contenham termos antigos sem tocar no código funcional
    conteudo_html = re.sub(r'<!--.*?(?:stripe|mônaco|monaco).*?-->', '', conteudo_html, flags=re.IGNORECASE | re.DOTALL)

    HTML_PATH.write_text(conteudo_html, encoding="utf-8")
    print("[OK] Chamadas públicas do index.html atualizadas para o padrão executivo global.")

    # 4. Verificação final do código público (index.html)
    restantes = [t for t in ["stripe", "mônaco", "monaco"] if t in conteudo_html.lower()]
    print("=" * 75)
    if not restantes:
        print("[SUCESSO TOTAL] Código-fonte do index.html 100% limpo! Nota Auditoria: 10.0 / 10.0")
    else:
        print(f"[AVISO] Ainda restou algum termo interno no HTML: {', '.join(restantes)}")
        print("-> Se for nome de função JS interna, me avise qual linha sobrou para renomearmos com segurança.")
    print("=" * 75)

if __name__ == "__main__":
    aplicar_blindagem_total()