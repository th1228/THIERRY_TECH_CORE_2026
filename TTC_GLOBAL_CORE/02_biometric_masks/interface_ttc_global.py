# -*- coding: utf-8 -*-
import customtkinter as ctk
try:
    import neuro_gravidade_preditor as engine
    print("Módulo 'neuro_gravidade_preditor' carregado com sucesso.")
except ImportError as e:
    print(f"ERRO CRÍTICO DE IMPORTAÇÃO: {e}")
    class MockEngine:
        def processar_bio_age(self, valor): return -1.0
    engine = MockEngine()

class ThierryTechDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações de Elite (Paleta Black & Gold & Neon)
        self.title("THIERRY TECHNOLOGY CONCEPT GLOBAL | ELITE SYSTEM")
        self.geometry("1200x780")
        ctk.set_appearance_mode("Dark")

        # Layout Grid
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------
        # 1. PAINEL DE CONTROLE (SIDEBAR)
        # ---------------------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#050505", border_width=1, border_color="#D4AF37")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(self.sidebar, text="TTC GLOBAL", font=("Montserrat", 28, "bold"), text_color="#D4AF37")
        self.logo.pack(pady=(40, 60))

        self.slider_label = ctk.CTkLabel(self.sidebar, text="DESVIO BIOLÓGICO (HADES SCORE)", font=("Consolas", 12), text_color="#00FFFF")
        self.slider_label.pack(pady=(20, 5))
        
        self.morph_slider = ctk.CTkSlider(self.sidebar, from_=0, to=100, number_of_steps=100, command=self.atualizar_analise_live, fg_color="#333", progress_color="#39FF14", button_color="#D4AF37", button_hover_color="#39FF14")
        self.morph_slider.pack(pady=10, padx=20)
        self.morph_slider.set(0)

        self.metric_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.metric_frame.pack(pady=40, padx=20)

        self.score_prefix = ctk.CTkLabel(self.metric_frame, text="SCORE ATUAL:", font=("Consolas", 14), text_color="#00FFFF")
        self.score_prefix.pack()

        self.metric_label = ctk.CTkLabel(self.metric_frame, text="0.00", font=("Consolas", 36, "bold"), text_color="#39FF14")
        self.metric_label.pack()

        self.action_btn = ctk.CTkButton(self.sidebar, text="GERAR LAUDO FORENSE", fg_color="transparent", border_width=1, border_color="#39FF14", text_color="#39FF14", font=("Montserrat", 14, "bold"), hover_color="#1a331a", corner_radius=20, height=40)
        self.action_btn.pack(side="bottom", pady=40, padx=20)

        # ---------------------------------------------------------
        # 2. PALCO FORENSE
        # ---------------------------------------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="#0a0a0a", border_width=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.visual_display = ctk.CTkLabel(self.main_frame, text="[SYSTEM READY - AGUARDANDO CAPTURA]", font=("Consolas", 14), text_color="#666")
        self.visual_display.pack(expand=True, fill="both")

    # ---------------------------------------------------------
    # FUNÇÃO DE CONEXÃO FINALIZADA
    # ---------------------------------------------------------
    def atualizar_analise_live(self, valor):
        """
        Esta função conecta o seu Slider ao Motor de Cálculo (engine).
        """
        # 1. Pega o valor do slider
        valor_int = int(valor)
        
        # 2. Envia para o seu motor de processamento (engine)
        # Supomos que seu arquivo neuro_gravidade_preditor tenha a função 'processar_bio_age'
        resultado = engine.processar_bio_age(valor_int)
        
        # 3. Atualiza a tela com o resultado que o motor devolveu
        # Formata o resultado para 2 casas decimais
        self.metric_label.configure(text=f"{resultado:.2f}")
        
        # Opcional: Feedback visual extra
        print(f"Análise em tempo real: Slider={valor_int} -> Resultado={resultado}")

if __name__ == "__main__":
    app = ThierryTechDashboard()
    app.mainloop()