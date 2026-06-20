import customtkinter as ctk
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        self.title("TTC Control Global")
        self.configure(fg_color="#000000")
        
        # Botão Neon
        self.btn = ctk.CTkButton(
            self, 
            text="SALVAR AGORA", 
            fg_color="#00FFCC", 
            text_color="black", 
            font=("Arial", 16, "bold"),
            command=self.enviar_sinal
        )
        self.btn.pack(pady=70)

    def enviar_sinal(self):
        # GARANTE que o arquivo vai para a pasta do seu projeto, não importa onde você clicou
        pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))
        caminho_sinal = os.path.join(pasta_do_projeto, "comando_captura.txt")
        
        with open(caminho_sinal, "w") as f:
            f.write("capturar")
        
        print(f"Sinal enviado com sucesso para: {caminho_sinal}")

if __name__ == "__main__":
    app = App()
    app.mainloop()