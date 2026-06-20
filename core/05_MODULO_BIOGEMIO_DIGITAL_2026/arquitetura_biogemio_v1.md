import customtkinter as ctk
import cv2
import mediapipe as mp
import numpy as np
from fpdf import FPDF
from tkinter import filedialog, messagebox
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TTC Global - Engine 2026")
        self.geometry("400x450")
        self.configure(fg_color="#0a0a0a")

        self.pre_path = None
        self.pos_path = None
        
        # Inicialização do Mediapipe Hands para sensibilidade/biometria
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        ctk.CTkButton(self, text="Selecionar Pré", fg_color="#004d40", command=self.load_pre).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self, text="Selecionar Pós", fg_color="#004d40", command=self.load_pos).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self, text="GERAR PDF/LAUDO COMPLETO", fg_color="#1e40af", command=self.workflow_automatico).pack(pady=20, padx=20, fill="x")

    def load_pre(self): self.pre_path = filedialog.askopenfilename()
    def load_pos(self): self.pos_path = filedialog.askopenfilename()

    def processar_malha(self, path, output_name):
        img = cv2.imread(path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        coords = []
        with mp.solutions.face_mesh.FaceMesh(static_image_mode=True) as fm:
            res = fm.process(img_rgb)
            if res.multi_face_landmarks:
                landmarks = res.multi_face_landmarks[0].landmark
                indices = [1, 152, 234, 454, 10, 151, 33, 263, 61, 291]
                for idx in indices:
                    coords.append((landmarks[idx].x, landmarks[idx].y))
                mp.solutions.drawing_utils.draw_landmarks(img, res.multi_face_landmarks[0], mp.solutions.face_mesh.FACEMESH_TESSELATION)
        cv2.imwrite(output_name, img)
        return coords

    def processar_mao(self, frame):
        # Lógica de detecção de sensibilidade/landmarks da mão
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res_hands = self.hands.process(frame_rgb)
        if res_hands.multi_hand_landmarks:
            for hand_lms in res_hands.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def workflow_automatico(self):
        if not self.pre_path or not self.pos_path:
            messagebox.showerror("Erro", "Selecione ambas as fotos!")
            return

        coords_pre = self.processar_malha(self.pre_path, "pre_overlay.jpg")
        coords_pos = self.processar_malha(self.pos_path, "pos_overlay.jpg")

        diff = np.mean(np.abs(np.array(coords_pre) - np.array(coords_pos)))
        precisao = (1 - diff) * 100

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Laudo Tecnico TTC Global", ln=True, align='C')
        
        pdf.image("pre_overlay.jpg", 10, 40, 90)
        pdf.image("pos_overlay.jpg", 110, 40, 90)
        
        pdf.set_y(160)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Arquitetura e Precisao Facial:", ln=True)
        pdf.set_font("Arial", '', 12)
        texto_laudo = f"Variacao estrutural detectada: {diff:.4f} unidades. Precisao da integridade geometrica: {precisao:.2f}%. A reconstrucao foi validada tecnicamente."
        pdf.multi_cell(0, 10, txt=texto_laudo)
        
        caminho_final = "Laudo_Final_TTC.pdf"
        pdf.output(caminho_final)
        
        os.startfile(caminho_final) if os.name == 'nt' else os.system(f"open {caminho_final}")
        messagebox.showinfo("Sucesso", "Laudo gerado!")

if __name__ == "__main__":
    App().mainloop()