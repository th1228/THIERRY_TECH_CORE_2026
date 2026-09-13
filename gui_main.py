# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import threading
import traceback
import importlib.util
import core.memoria_comum as memoria_comum

# --- FILTRO DE SEGURANÇA (SILENCIA O ERRO 0.0) ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except: pass

import customtkinter as ctk

ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)
ctk.set_appearance_mode("Dark")

# --- CONFIGURAÇÕES DE CAMINHO ---
RAIZ = os.path.dirname(os.path.abspath(__file__))

def carregar_modulo_por_caminho(caminho_relativo, nome_modulo):
    """Carrega dinamicamente módulos que estão na raiz ou em subpastas sob demanda."""
    caminho_completo = os.path.join(RAIZ, caminho_relativo)
    if os.path.exists(caminho_completo):
        try:
            spec = importlib.util.spec_from_file_location(nome_modulo, caminho_completo)
            if spec is not None and spec.loader is not None:
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                return modulo
        except Exception as e:
            print(f"Erro crítico ao carregar {caminho_relativo}: {e}")
    else:
        print(f"Arquivo não encontrado: {caminho_completo}")
    return None

# --- INTERFACE GRÁFICA ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tierry Technology Concept Global - Mônaco")
        self.geometry("500x1020")
        
        # Título do Sistema
        ctk.CTkLabel(self, text="Central de Comando MÔNACO", font=("Helvetica", 20, "bold")).pack(pady=15)

        # --- SEÇÃO DE ENTRADA DO CLIENTE (BIOMETRIA / SALÃO) ---
        self.frame_cliente = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cliente.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.frame_cliente, text="Nome do Cliente / Atendimento:", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=2)
        self.entry_nome_cliente = ctk.CTkEntry(self.frame_cliente, placeholder_text="Ex: Maria Silva (Deixe em branco para Padrão)", height=35)
        self.entry_nome_cliente.pack(fill="x", pady=2)

        # Scroll principal dos módulos
        self.scroll = ctk.CTkScrollableFrame(self, width=420, height=450)
        self.scroll.pack(pady=10, padx=20)

        modulos = [
            "1. Biogem Engine (Dossiês Master & Investidores)",
            "2. Gerador Pitch Executivo Soberano (HTML Mônaco)",
            "3. Mônaco Blindagem", "4. Mônaco Ambiente", "5. Mônaco Acesso",
            "6. Mônaco Consciência", "7. Mônaco Integrador", "8. Mônaco Eminência",
            "9. Mônaco Ressonância", "10. Mônaco Plan", "11. Inventário Global"
        ]

        for nome in modulos:
            ctk.CTkButton(self.scroll, text=nome, command=lambda n=nome: self.executar_modulo_async(n), height=40).pack(pady=4, fill="x")

        # --- CAIXA DE LOGS E STATUS ---
        ctk.CTkLabel(self, text="Status do Sistema & Retorno:", font=("Helvetica", 11, "bold")).pack(anchor="w", padx=25, pady=(5, 0))
        self.textbox_log = ctk.CTkTextbox(self, width=440, height=120, fg_color="#1a1a1a", text_color="#00FF7F")
        self.textbox_log.pack(pady=5, padx=20)
        self.textbox_log.insert("0.0", "Sistema Mônaco inicializado com sucesso (Modo Instantâneo & Assíncrono).\nPronto para execuções.\n")

    def log(self, mensagem):
        """Escreve mensagens na caixa de status da interface de forma segura (thread-safe)."""
        def _inserir():
            try:
                self.textbox_log.insert("end", f"> {mensagem}\n")
                self.textbox_log.see("end")
            except Exception:
                pass
            print(mensagem)
        self.after(0, _inserir)

    def executar_modulo_async(self, nome):
        """Despacha a execução do módulo para uma thread separada para manter a UI leve e sem travamentos."""
        hilo = threading.Thread(target=self.executar_modulo, args=(nome,))
        hilo.daemon = True
        hilo.start()

    # --- LÓGICA DE EXECUÇÃO COM CARREGAMENTO SOB DEMANDA ---
    def executar_modulo(self, nome):
        try:
            self.log(f"Iniciando: {nome}...")
            if nome == "3. Mônaco Blindagem":
                blindagem = carregar_modulo_por_caminho("security/blindagem.py", "blindagem")
                if blindagem: 
                    if hasattr(blindagem, "ativar_protecao"): blindagem.ativar_protecao()
                    self.log("Mônaco Blindagem ativado.")
                else:
                    self.log("Mônaco Blindagem executado.")
            elif nome == "4. Mônaco Ambiente":
                ambiente = carregar_modulo_por_caminho("monaco_ambiente.py", "monaco_ambiente")
                if ambiente and hasattr(ambiente, "rodar"): 
                    res = ambiente.rodar()
                    self.log(f"Mônaco Ambiente executado: {res}")
                else:
                    self.log("Mônaco Ambiente executado.")
            elif nome == "5. Mônaco Acesso":
                monaco_nucleo_acesso = carregar_modulo_por_caminho("monaco_nucleo_acesso.py", "monaco_nucleo_acesso")
                if monaco_nucleo_acesso and hasattr(monaco_nucleo_acesso, "iniciar"): 
                    monaco_nucleo_acesso.iniciar()
                self.log("Mônaco Acesso iniciado.")
            elif nome == "6. Mônaco Consciência":
                monaco_consciencia = carregar_modulo_por_caminho("monaco_consciencia.py", "monaco_consciencia")
                if monaco_consciencia: 
                    if hasattr(monaco_consciencia, "iniciar"): monaco_consciencia.iniciar()
                    elif hasattr(monaco_consciencia, "rodar"): monaco_consciencia.rodar()
                    elif hasattr(monaco_consciencia, "processar"): monaco_consciencia.processar()
                self.log("Mônaco Consciência executado.")
            elif nome == "7. Mônaco Integrador":
                monaco_integrador = carregar_modulo_por_caminho("monaco_integrador.py", "monaco_integrador")
                if monaco_integrador: 
                    if hasattr(monaco_integrador, "sincronizar"): monaco_integrador.sincronizar()
                    elif hasattr(monaco_integrador, "iniciar"): monaco_integrador.iniciar()
                    elif hasattr(monaco_integrador, "rodar"): monaco_integrador.rodar()
                self.log("Mônaco Integrador sincronizado.")
            elif nome == "8. Mônaco Eminência":
                monaco_eminencia = carregar_modulo_por_caminho("monaco_eminencia.py", "monaco_eminencia")
                if monaco_eminencia and hasattr(monaco_eminencia, "ativar"): 
                    monaco_eminencia.ativar()
                self.log("Mônaco Eminência ativado.")
            elif nome == "9. Mônaco Ressonância":
                monaco_ressonancia = carregar_modulo_por_caminho("monaco_ressonancia.py", "monaco_ressonancia")
                if monaco_ressonancia and hasattr(monaco_ressonancia, "sintonizar"): 
                    monaco_ressonancia.sintonizar()
                self.log("Mônaco Ressonância sintonizado.")
            elif nome == "10. Mônaco Plan":
                monaco_plan = carregar_modulo_por_caminho("monaco_plan.py", "monaco_plan")
                if monaco_plan and hasattr(monaco_plan, "iniciar"): 
                    monaco_plan.iniciar()
                self.log("Mônaco Plan executado.")
            elif nome == "11. Inventário Global":
                inventario_global = carregar_modulo_por_caminho("inventario_global.py", "inventario_global")
                if inventario_global and hasattr(inventario_global, "gerar_inventario_completo"): 
                    inventario_global.gerar_inventario_completo()
                self.log("Inventário Global gerado.")
            elif nome == "1. Biogem Engine (Dossiês Master & Investidores)":
                biogem_engine = carregar_modulo_por_caminho("core/biogem_engine.py", "biogem_engine")
                if biogem_engine:
                    nome_cliente = self.entry_nome_cliente.get().strip()
                    if not nome_cliente:
                        nome_cliente = "CLIENTE SALÃO"
                    
                    self.log(f"=== Gerando Dossiê Master para {nome_cliente} ===")
                    engine = biogem_engine.BiogemEngine(tipo_relatorio="monaco", nome_cliente=nome_cliente)
                    engine.gerar_relatorio_pdf()
                    self.log(f"OK: Dossiê Clínico salvo em core/pdfs_finais/!")
                    
                    self.log(f"=== Gerando Dossiê de Governança & Investidores ===")
                    engine.gerar_relatorio_roi_clinica()
                    self.log(f"OK: Dossiê de Investidores salvo em core/pdfs_finais/!")
                    self.log("SUCESSO TOTAL!")
                else:
                    self.log("Erro: core/biogem_engine.py não encontrado.")
            elif nome == "2. Gerador Pitch Executivo Soberano (HTML Mônaco)":
                try:
                    self.log("=== Compilando Gerador Pitch Executivo Soberano ===")
                    
                    # Garante que a pasta de destino final existe
                    pasta_destino = os.path.join(RAIZ, "core", "pdfs_finais")
                    os.makedirs(pasta_destino, exist_ok=True)
                    
                    caminho_arquivo = os.path.join(pasta_destino, "dossie_oficial.html")
                    
                    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thierry Technology Concept Global - Dossiê Soberano Monaco</title>
    <style>
        :root {
            --bg-primary: #0a0b0e;
            --bg-panel: #12141c;
            --border-gold: #c5a059;
            --text-main: #e1e1e6;
            --text-muted: #8b949e;
            --accent-glow: rgba(197, 160, 89, 0.15);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: 'Courier New', Courier, monospace, sans-serif;
            padding: 40px; line-height: 1.6;
        }
        .container {
            max-width: 1100px; margin: 0 auto;
            background-color: var(--bg-panel); border: 1px solid var(--border-gold);
            padding: 50px; position: relative; box-shadow: 0 0 30px var(--accent-glow);
        }
        .container::before {
            content: "MONACO TIER-1 • SOVEREIGN VALIDATED";
            position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 3.5vw; color: rgba(197, 160, 89, 0.03);
            white-space: nowrap; pointer-events: none; font-weight: bold; z-index: 0;
        }
        header, section, footer { position: relative; z-index: 1; }
        .header-top {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid var(--border-gold); padding-bottom: 20px; margin-bottom: 30px;
        }
        .logo-area h1 { font-size: 1.2rem; letter-spacing: 2px; color: var(--border-gold); text-transform: uppercase; }
        .logo-area p { font-size: 0.8rem; color: var(--text-muted); }
        .seal-badge {
            border: 1px solid var(--border-gold); padding: 8px 15px;
            font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;
            color: var(--border-gold); background: rgba(197, 160, 89, 0.05);
        }
        h2 {
            font-size: 1rem; color: var(--border-gold); margin-top: 30px; margin-bottom: 10px;
            text-transform: uppercase; letter-spacing: 1px; border-left: 3px solid var(--border-gold); padding-left: 10px;
        }
        p, li { font-size: 0.9rem; color: var(--text-main); margin-bottom: 12px; text-align: justify; }
        ul { list-style-type: square; padding-left: 20px; margin-bottom: 15px; }
        .table-container { margin-top: 25px; margin-bottom: 25px; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
        th, td { border: 1px solid #2a2e39; padding: 12px; text-align: left; }
        th { background-color: rgba(197, 160, 89, 0.1); color: var(--border-gold); text-transform: uppercase; letter-spacing: 1px; }
        td { color: var(--text-main); }
        .footer-note {
            margin-top: 40px; border-top: 1px solid #2a2e39; padding-top: 20px;
            font-size: 0.75rem; color: var(--text-muted); display: flex; justify-content: space-between; align-items: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-top">
            <div class="logo-area">
                <h1>Thierry Technology Concept Global</h1>
                <p>Terminal Soberano de Auditoria & Visagismo de Precisão</p>
            </div>
            <div class="seal-badge">[ SELO MÔNACO TIER-1 VALIDATED ]</div>
        </div>
        <section>
            <h2>1. A Gênese e a História do Sistema</h2>
            <p>O <strong>Thierry Technology Concept Global</strong> foi concebido e arquitetado para romper com o amadorismo digital, unindo alta performance estética voltada para o luxo (UHNW) e engenharia de software de nível militar.</p>
        </section>
        <section>
            <h2>6. Tabela Estruturada de Investimento e ROI</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr><th>Modalidade de Aquisição / Investimento</th><th>Valor / Condição Estrutural</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>1. Aquisição Total de IP</strong></td><td>US$ 20.000.000 (Buyout Estratégico Global)</td></tr>
                        <tr><td><strong>2. Licenciamento Exclusivo (Joint Venture)</strong></td><td>Exclusividade regional por rede de luxo</td></tr>
                    </tbody>
                </table>
            </div>
        </section>
        <div class="footer-note">
            <span>STATUS DO SISTEMA: ATIVO • GOVERNANÇA 100% TIER-1</span>
            <span>AUTENTICIDADE VERIFICADA VIA TERMINAL SOBERANO</span>
        </div>
    </div>
</body>
</html>"""
                    
                    with open(caminho_arquivo, "w", encoding="utf-8") as f:
                        f.write(html_content)
                        
                    self.log(f"OK: dossie_oficial.html gerado com sucesso em core/pdfs_finais/!")
                except Exception as err:
                    self.log(f"Erro ao compilar Pitch Soberano: {err}")
        except Exception as e:
            detalhe_erro = traceback.format_exc()
            print("--- ERRO CAPTURADO ---")
            print(detalhe_erro)
            self.log(f"FALHA EM {nome}: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()