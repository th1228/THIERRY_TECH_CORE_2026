import customtkinter as ctk
import cv2
from PIL import Image
import datetime

class InterfaceDual(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Thierry Technology Concept Global - Neurogravidade Preditivo")
        self.geometry("1100x600")

        # Layout: Lado esquerdo (Captura) | Lado direito (Resultados)
        self.frame_esq = ctk.CTkFrame(self, width=500, height=500)
        self.frame_esq.pack(side="left", padx=20, pady=20)

        self.frame_dir = ctk.CTkFrame(self, width=500, height=500)
        self.frame_dir.pack(side="right", padx=20, pady=20)

        self.btn = ctk.CTkButton(self, text="Iniciar Análise Global", command=self.processar)
        self.btn.pack(pady=20)

    def processar(self):
        # 1. Captura da Câmera
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            # 2. Lógica Interna de Neurogravidade (Aqui você insere o cálculo matemático)
            # Como você quer tudo aqui, o processamento ocorre direto nesta função
            dados_analise = "Análise Forense: Gravidade Facial 8.2\nBio-Age: 34 anos\nStatus: Integração Concluída"
            
            # 3. Exibir imagem capturada
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 300))
            
            label_img = ctk.CTkLabel(self.frame_esq, image=img_tk, text="")
            label_img.image = img_tk
            label_img.pack()

            # 4. Exibir o parecer final no lado direito
            label_dados = ctk.CTkLabel(self.frame_dir, text=dados_analise, font=("Arial", 16))
            label_dados.pack(pady=20)

if __name__ == "__main__":
    app = InterfaceDual()
    app.mainloop()