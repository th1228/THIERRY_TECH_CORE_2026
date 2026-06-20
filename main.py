# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os
import motor_dados 

class HubCentral(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("TTC GLOBAL | HUB DE COMANDO 2026")
        self.geometry("500x750")
        self.configure(bg="black")
        
        self.configurar_atendimento()
        self.criar_menu()

    def configurar_atendimento(self):
        nome = simpledialog.askstring("TTC Global", "Nome do Cliente:")
        idioma = simpledialog.askstring("TTC Global", "Idioma (PT, EN, FR):").upper()
        # O motor_dados garante que esses dados fiquem persistentes para os outros scripts
        motor_dados.salvar("cliente_nome", nome)
        motor_dados.salvar("idioma", idioma)

    def criar_menu(self):
        botoes = [
            ("1. Visagismo & Osteometria", "osteometria.py"),
            ("2. BioGênio Digital", "biogenio_engine.py"),
            ("3. Tricologia Clínica", "tricologia.py"),
            ("4. Fenotipagem Neural", "fenotipagem.py"),
            ("5. Monitoramento Ambiental", "clima.py"),
            ("6. ATELIER MÔNACO PLAN", "INTEGRAR_MONACO"),
            ("7. GERAR LAUDO FINAL", "core/gerador_relatorio_definitivo.py")
        ]

        for texto, comando in botoes:
            btn = tk.Button(self, text=texto, bg="#1a1a1a", fg="gold", 
                            font=("Helvetica", 12, "bold"),
                            command=lambda c=comando: self.executar_acao(c))
            btn.pack(pady=10, fill='x', padx=60)

    def executar_acao(self, comando):
        # 1. Integração Especial Mônaco
        if comando == "INTEGRAR_MONACO":
            senha = simpledialog.askstring("Segurança", "Chave de Acesso Mônaco:")
            if senha == "MÔNACO2026":
                # Executa o integrador usando o caminho relativo correto
                subprocess.Popen(["python", "monaco_integrador.py"])
            else:
                messagebox.showerror("Acesso Negado", "Chave Inválida.")
        
        # 2. Execução de todos os outros módulos (incluindo o gerador)
        else:
            if os.path.exists(comando):
                subprocess.Popen(["python", comando])
            else:
                messagebox.showerror("Erro", f"Arquivo {comando} não encontrado!")

if __name__ == "__main__":
    app = HubCentral()
    app.mainloop()