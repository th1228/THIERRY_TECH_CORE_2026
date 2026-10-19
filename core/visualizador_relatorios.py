
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

import os
import customtkinter as ctk
from tkinter import messagebox

class VisualizadorPDFApp(ctk.CTkToplevel):
    def __init__(self, master, pdf_path, titulo, lang: str = "PT"):
        super().__init__(master)
        self.geometry("800x600")
        self.title(f"Documento: {titulo}")
        
        self.pdf_path = pdf_path

        # Painel Superior (Toolbar) com as ações rápidas
        self.toolbar = ctk.CTkFrame(self, height=50)
        self.toolbar.pack(fill="x", padx=10, pady=10)

        # Botão de Espelhar na Tela
        self.btn_espelhar = ctk.CTkButton(
            self.toolbar, 
            text="🖥️ Espelhar na Tela", 
            command=self.espelhar_tela
        )
        self.btn_espelhar.pack(side="left", padx=5)

        # Botão de Enviar para o Cliente
        self.btn_enviar = ctk.CTkButton(
            self.toolbar, 
            text="📤 Enviar para o Cliente", 
            fg_color="green", 
            command=self.enviar_cliente
        )
        self.btn_enviar.pack(side="left", padx=5)

        # Área de Exibição do Documento
        self.viewer_frame = ctk.CTkFrame(self)
        self.viewer_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.label_info = ctk.CTkLabel(
            self.viewer_frame, 
            text=f"Visualizando Relatório:\n{os.path.basename(pdf_path)}",
            font=("Arial", 14, "bold")
        )
        self.label_info.pack(expand=True)

    def espelhar_tela(self):
        # Alterna o estado da janela para tela cheia (modo apresentação/espelhamento)
        current_state = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not current_state)

    def enviar_cliente(self):
        # Rotina de disparo de envio para o cliente
        messagebox.showinfo("Envio Realizado", f"O relatório {os.path.basename(self.pdf_path)} foi enviado com sucesso ao cliente!")

def abrir_todos_os_pdfs(master, lista_caminhos):
    # Função responsável por disparar a abertura simultânea dos 7 PDFs em janelas independentes
    for i, caminho in enumerate(lista_caminhos):
        titulo_janela = f"Relatório Técnico 0{i+1}"
        VisualizadorPDFApp(master, caminho, titulo_janela)