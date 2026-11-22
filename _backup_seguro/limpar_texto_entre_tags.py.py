# -*- coding: utf-8 -*-
import re
import shutil
from pathlib import Path

HTML_PATH = Path("index.html")
BACKUP_PATH = Path("index.html.pre_tags.bak")

def limpar_apenas_entre_tags():
    if not HTML_PATH.exists():
        print("[ERRO] index.html não encontrado na raiz.")
        return

    shutil.copy2(HTML_PATH, BACKUP_PATH)
    conteudo = HTML_PATH.read_text(encoding="utf-8")

    # Separa o arquivo preservando <script> e <style> intactos
    partes = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)', conteudo, flags=re.IGNORECASE | re.DOTALL)

    def substituir_texto_visivel(trecho_html):
        # Troca palavras APENAS fora das tags HTML (entre '>' e '<')
        def limpar_conteudo_tag(match):
            texto = match.group(0)
            texto = re.sub(r'Monte Carlo', 'Europa Central', texto, flags=re.IGNORECASE)
            texto = re.sub(r'Mônaco|Monaco', 'Global', texto, flags=re.IGNORECASE)
            texto = re.sub(r'Stripe', 'Gateway Executivo', texto, flags=re.IGNORECASE)
            return texto

        return re.sub(r'>[^<]+<', limpar_conteudo_tag, trecho_html)

    # Aplica apenas nos blocos que não são <script> nem <style>
    resultado = []
    for parte in partes:
        if parte.lower().startswith(('<script', '<style')):
            resultado.append(parte)
        else:
            resultado.append(substituir_texto_visivel(parte))

    HTML_PATH.write_text(''.join(resultado), encoding="utf-8")
    print("=" * 75)
    print("[SUCESSO] Textos visíveis entre tags limpos sem tocar em CSS, IDs ou JS!")
    print("=" * 75)

if __name__ == "__main__":
    limpar_apenas_entre_tags()