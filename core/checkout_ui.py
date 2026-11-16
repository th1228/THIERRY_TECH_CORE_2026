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

import customtkinter as ctk
from tkinter import filedialog, messagebox

def abrir_janela_checkout():
    janela_checkout = ctk.CTkToplevel()
    janela_checkout.title("TTC Global - Sovereign Activation")
    janela_checkout.geometry("450x550")
    janela_checkout.configure(fg_color="#050505")
    janela_checkout.attributes("-topmost", True)
    janela_checkout.resizable(False, False)

    lbl_titulo = ctk.CTkLabel(janela_checkout, text="ATIVAÇÃO DE LICENÇA", 
                              font=("Helvetica", 20, "bold"), text_color="#d4af37")
    lbl_titulo.pack(pady=(30, 10))

    tabview = ctk.CTkTabview(janela_checkout, fg_color="#121212", 
                             segmented_button_selected_color="#d4af37", 
                             text_color="#ffffff")
    tabview.pack(padx=20, pady=10, fill="both", expand=True)

    aba_br = tabview.add("Nacional (Pix)")
    aba_intl = tabview.add("Mônaco Plan")

    # Aba Nacional
    ctk.CTkLabel(aba_br, text="Pagamento Instantâneo via Pix", text_color="#a0a0a0").pack(pady=20)
    
    # Aba Internacional
    ctk.CTkLabel(aba_intl, text="Transferência via SWIFT/IBAN", text_color="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=10)
    frame_dados = ctk.CTkFrame(aba_intl, fg_color="#0a0a0a", border_color="#333333", border_width=1)
    frame_dados.pack(pady=10, padx=15, fill="x")
    ctk.CTkLabel(frame_dados, text="IBAN: PT50 0000 0000 0000 0000", text_color="#d4af37").pack(pady=10)

    def anexar_comprovante():
        filedialog.askopenfilename()
        messagebox.showinfo("Sucesso", "Comprovante enviado. Aguarde auditoria.")

    ctk.CTkButton(aba_intl, text="Anexar Comprovante", command=anexar_comprovante, fg_color="#d4af37", text_color="black").pack(pady=20)

# --- DISPARADOR (Isso faz a janela aparecer) ---
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1x1") # Janela raiz invisível
    app.withdraw()
    abrir_janela_checkout()
    app.mainloop()