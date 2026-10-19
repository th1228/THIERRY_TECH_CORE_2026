# --- PONTE DE MEMÓRIA AUTOMÁTICA (THIERRY TECH) ---
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    try:
        from core.memoria_comum import instancia_memoria as memoria
    except ImportError:
        class MemoriaMock:
            def salvar_dados(self, chave, valor): pass
            def registrar(self, chave, valor): pass
            def ler_dados(self, chave): return None
        memoria = MemoriaMock()
# ---------------------------------------------------

# -*- coding: utf-8 -*-
"""
THIÉRRY TECHNOLOGY CONCEPT GLOBAL - GARÇOM/PONTE (FLASK APP)
Responsável por servir o painel HTML, escutar os gatilhos dos botões
e delegar a compilação soberana para o main.py / motores de Mônaco.
"""

from flask import Flask, render_template, request, send_file, jsonify
import os
import sys
from pathlib import Path

# Garante a resolução correta dos caminhos na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Importa o script principal de orquestração (main.py)
import main

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def pagina_inicial():
    """Renderiza o painel web principal do ecossistema TCC Global."""
    return render_template('painel_web.html')

@app.route('/gerar-pdf', methods=['POST'])
def acao_gerar_pdf():
    """
    Rota acionada pelo painel HTML. 
    Captura os parâmetros do formulário/botão e delega a compilação para o orquestrador do main.py.
    """
    try:
        # 1. Pega as informações enviadas pelo painel HTML (via form ou JSON)
        dados_html = request.form.to_dict()
        if not dados_html and request.is_json:
            dados_html = request.get_json() or {}

        print(f"[FLASK PONTE] Recebidos dados do painel HTML: {dados_html}")
        
        # Extrai os parâmetros com valores padrão seguros
        tipo_relatorio = dados_html.get('tipo', dados_html.get('relatorio', 'modelo_matematico'))
        cliente = dados_html.get('cliente', 'THIÉRRY RODRIGUES')
        empresa = dados_html.get('empresa', 'TTC Global Corp')
        email = dados_html.get('email', 'theiry10rd@gmail.com')

        # 2. Delega a compilação cirúrgica diretamente para a função oficial do main.py
        caminho_do_pdf_str = main.compilar_pdf_especifico(
            tipo_limpo=tipo_relatorio,
            nome_cli=cliente,
            empresa_cli=empresa,
            email_cli=email
        )
        
        caminho_do_pdf = Path(caminho_do_pdf_str)

        # 3. Retorna o PDF gerado diretamente para o navegador do usuário
        if caminho_do_pdf and caminho_do_pdf.exists():
            return send_file(
                str(caminho_do_pdf), 
                mimetype='application/pdf',
                as_attachment=True,
                download_name=caminho_do_pdf.name
            )
        else:
            return jsonify({"status": "erro", "detalhe": "O arquivo PDF gerado não foi encontrado no cofre."}), 404

    except (ValueError, KeyError, TypeError) as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "erro", "detalhe": str(e)}), 500
    except (FileNotFoundError, PermissionError, OSError) as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "erro", "detalhe": str(e)}), 500
    except RuntimeError as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "erro", "detalhe": str(e)}), 500

if __name__ == '__main__':
    print("[FLASK APP] Inicializando Ponte Garçom na porta 5000...")
    app.run(host='127.0.0.1', port=5000, debug=True)
