import customtkinter as ctk
import random
import sys
import os

# Adiciona a pasta 'neural_core' ao caminho de busca
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'neural_core'))

try:
    import analise
except ImportError:
    analise = None

class ThierryMainInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Thierry Technology Concept Global - Forensic Division")
        self.geometry("1400x800")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#000000")
        self.neon_cyan = "#00FFFF"
        self.gold_accent = "#FFD700"
        self.metric_phi = None
        self.metric_dev = None
        self.metric_depth = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.setup_osteometric_panel()
        self.setup_pattern_panel()

    def setup_osteometric_panel(self):
        self.left_frame = ctk.CTkFrame(self, fg_color="#0A0A0A", border_width=3, border_color=self.neon_cyan, corner_radius=15)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        ctk.CTkLabel(self.left_frame, text="BIO-HARMONIZATION SCAN", font=("Arial", 22, "bold"), text_color=self.neon_cyan).pack(pady=(25, 10))
        data_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        data_frame.pack(fill="x", padx=15, pady=10)
        data_frame.grid_columnconfigure((0, 1), weight=1)

        def create_metric(label_text, value_text, row):
            ctk.CTkLabel(data_frame, text=label_text, font=("Arial", 14), text_color="#777777").grid(row=row, column=0, sticky="w", pady=5)
            val = ctk.CTkLabel(data_frame, text=value_text, font=("Arial", 18, "bold"), text_color=self.gold_accent)
            val.grid(row=row, column=1, sticky="e", pady=5)
            return val

        self.metric_phi = create_metric("PHI ALIGNMENT (X):", "0.618", 0)
        self.metric_dev = create_metric("HARMONIC DEVIATION:", "0.02μ", 1)
        self.metric_depth = create_metric("BIO-DYNAMIC DEPTH:", "14.2mm", 2)
        
        ctk.CTkButton(
            self.left_frame, text="SYNCHRONIZE BIO-FLOW", font=("Arial", 16, "bold"),
            fg_color="transparent", text_color=self.neon_cyan, border_width=2,
            border_color=self.neon_cyan, corner_radius=15,
            command=self.execute_analysis
        ).pack(side="bottom", fill="x", padx=15, pady=25)

    def setup_pattern_panel(self):
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color="#050505", border_width=2, border_color=self.neon_cyan, corner_radius=15)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        ctk.CTkLabel(self.right_frame, text="PATTERN LIBRARY / SCANNER", font=("Arial", 22, "bold"), text_color=self.neon_cyan).pack(pady=15)
        pattern_grid = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        pattern_grid.pack(fill="both", padx=10, pady=10)
        for i in range(15):
            btn = ctk.CTkButton(pattern_grid, text=f"TEX_{i+1:02d}", width=120, height=120, fg_color="#1A1A1A", border_width=2, border_color=self.gold_accent, corner_radius=10, hover_color="#333333")
            btn.grid(row=i//3, column=i%3, padx=8, pady=8)
        ctk.CTkLabel(self.right_frame, text="SCANNER STATUS: ACTIVE", text_color=self.neon_cyan).pack(pady=(20, 5))
        bar = ctk.CTkProgressBar(self.right_frame, fg_color="#222222", progress_color=self.gold_accent)
        bar.pack(fill="x", padx=15, pady=(0, 20))
        bar.set(0.85)

    def execute_analysis(self):
        if analise:
            try:
                dados = analise.realizar_leitura()
                self.metric_phi.configure(text=str(dados["simetria_facial"]))
                self.metric_dev.configure(text=f"{dados['angulo_mandibular']}°")
                self.metric_depth.configure(text=f"{dados['distancia_orbita']}mm")
                analise.exportar_laudo(dados)
            except Exception as e:
                print(f"[ERRO] {e}")
        else:
            self.metric_phi.configure(text=str(round(random.uniform(0.6, 0.63), 3)))

if __name__ == "__main__":
    app = ThierryMainInterface()
    app.mainloop()