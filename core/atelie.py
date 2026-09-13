# -*- coding: utf-8 -*-
import os
import sys
from typing import Optional, Dict, Any, Union
from fpdf import FPDF  # type: ignore

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria  # type: ignore
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave: str, valor: Any) -> None: pass
        def ler_dados(self, chave: str) -> Optional[Dict[str, Any]]: return None
    memoria = MemoriaMock()
# -----------------------------------------------

def gerar_diagnostico_final() -> str:
    """Gera o laudo em PDF integrando os dados da Memória Comum 🧠."""
    # 1. Busca segura de dados na Memória Comum
    rosto = memoria.ler_dados("ROSTO_STATUS") or {"FORMATO": "Sovereign Active"}
    cabelo = memoria.ler_dados("CABELO_DIAGNOSTICO") or {
        "VITALIDADE_SCORE": "Sovereign Active", 
        "REFLEXO": "Sovereign Active",
        "SAUDE_COURO": "Sovereign Active"
    }
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "THIERRY TECHNOLOGY - SUPREMACY NETWORK", ln=True, align='C')
    pdf.ln(10) # type: ignore
    
    # 2. Diagnóstico Técnico
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "LAUDO DE VISAGISMO E SAUDE CAPILAR:", ln=True)
    pdf.set_font("Arial", size=12)
    
    conteudo = (
        f"FORMATO DE ROSTO: {rosto.get('FORMATO', 'Sovereign Active')}\n"
        f"VITALIDADE DO FIO: {cabelo.get('VITALIDADE_SCORE', 'Sovereign Active')}/10\n"
        f"REFLEXO (LUMINOSIDADE): {cabelo.get('REFLEXO', 'Sovereign Active')}\n"
        f"SAUDE DO COURO CABELUDO: {cabelo.get('SAUDE_COURO', 'Sovereign Active')}\n"
    )
    pdf.multi_cell(190, 10, conteudo)
    
    # 3. Recomendação Estratégica
    pdf.ln(5) # type: ignore
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, "SUGESTAO DE ESTILO:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(190, 10, "Com base na analise, sugerimos cortes que tragam equilibrio a geometria facial detectada.")
    
    # Gerar arquivo na pasta correta do projeto
    pasta = os.path.join(ROOT_DIR, "Relatorios")
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, "Laudo_Supremacy.pdf")
    pdf.output(caminho)
    
    caminho_absoluto = os.path.abspath(caminho)
    
    # Sincronização automática com a Memória Comum 🧠
    try:
        memoria.salvar_dados("laudo_supremacy_pdf", {
            "caminho": caminho_absoluto,
            "status": "GERADO_COM_SUCESSO"
        })
    except Exception:
        pass
        
    print(f"\n[ATELIÊ] Laudo gerado com sucesso em: {caminho_absoluto}")
    return caminho_absoluto

def processar(frame: Optional[Any] = None) -> Dict[str, Union[str, Any]]:
    """Função de compatibilidade direta com o orquestrador (main.py) 💻."""
    caminho_pdf = gerar_diagnostico_final()
    return {
        "status": "Laudo gerado e integrado",
        "caminho_pdf": caminho_pdf
    }

if __name__ == "__main__":
    gerar_diagnostico_final()