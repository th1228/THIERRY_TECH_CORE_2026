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

# -*- coding: utf-8 -*-
import sys, os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# 🧠 Integração com a Memória Comum
try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()

# Dicionário mestre com os 7 tipos de rosto
MATRIZ_ESTILO = {
    "OVAL": {
        "MASCULINO": {"MEDIO": {"corte": "Pompadour Executivo", "descricao": "Volume moderado para valorizar a simetria."}},
        "FEMININO": {"MEDIO": {"corte": "Long Bob com Ondas", "descricao": "Emoldura a face com leveza."}},
        "AFRO": {"MEDIO": {"corte": "TWA Definido", "descricao": "Valoriza a coroa e curvatura natural."}},
        "INFANTIL": {"MEDIO": {"corte": "Curto Prático", "descricao": "Fácil manutenção e conforto."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Chanel Clássico", "descricao": "Elegância atemporal."}}
    },
    "REDONDO": {
        "MASCULINO": {"MEDIO": {"corte": "Undercut com Topo Alto", "descricao": "Laterais batidas para alongar o rosto."}},
        "FEMININO": {"MEDIO": {"corte": "Chanel de Bico Longo", "descricao": "Pontas frontais que estreitam as bochechas."}},
        "AFRO": {"MEDIO": {"corte": "Afro High Top", "descricao": "Volume direcionado para o topo."}},
        "INFANTIL": {"MEDIO": {"corte": "Raspado Lateral", "descricao": "Moderno e confortável."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Pixie com Volume", "descricao": "Eleva o centro visual."}}
    },
    "QUADRADO": {
        "MASCULINO": {"MEDIO": {"corte": "Textured Crop", "descricao": "Suaviza a rigidez da mandíbula."}},
        "FEMININO": {"MEDIO": {"corte": "Shag Hair", "descricao": "Camadas fluidas que suavizam os cantos."}},
        "AFRO": {"MEDIO": {"corte": "Black Power Arredondado", "descricao": "Linhas circulares que suavizam o maxilar."}},
        "INFANTIL": {"MEDIO": {"corte": "Curto Clássico", "descricao": "Simples e arrumado."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Bob Médio Desestruturado", "descricao": "Leveza sem marcações duras."}}
    },
    "CORACAO": {
        "MASCULINO": {"MEDIO": {"corte": "Medium Sweep Back", "descricao": "Volume lateral para harmonia."}},
        "FEMININO": {"MEDIO": {"corte": "Long Bob Modelado", "descricao": "Compensa a largura superior."}},
        "AFRO": {"MEDIO": {"corte": "Corte Médio com Franja", "descricao": "Suaviza a testa proeminente."}},
        "INFANTIL": {"MEDIO": {"corte": "Chanel com Base Reta", "descricao": "Suaviza o formato."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Chanel Suave", "descricao": "Elegância e equilíbrio."}}
    },
    "TRIANGULAR": {
        "MASCULINO": {"MEDIO": {"corte": "Ivy League Volumoso", "descricao": "Equilibra a mandíbula larga."}},
        "FEMININO": {"MEDIO": {"corte": "Chanel com Volume na Coroa", "descricao": "Gera proporção."}},
        "AFRO": {"MEDIO": {"corte": "Tapered Cut", "descricao": "Equilibra mandíbula e coroa."}},
        "INFANTIL": {"MEDIO": {"corte": "Chanel Leve", "descricao": "Suaviza os traços."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Bob Elegante", "descricao": "Sofisticação e equilíbrio."}}
    },
    "DIAMANTE": {
        "MASCULINO": {"MEDIO": {"corte": "Messy Fringe", "descricao": "Movimento frontal para equilibrar."}},
        "FEMININO": {"MEDIO": {"corte": "Bob Desestruturado", "descricao": "Preenche a região do queixo."}},
        "AFRO": {"MEDIO": {"corte": "Black Power Lateralizado", "descricao": "Equilibra as maçãs do rosto."}},
        "INFANTIL": {"MEDIO": {"corte": "Chanel Desfiado", "descricao": "Movimento e suavidade."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Bob com Ondas", "descricao": "Elegância acolhedora."}}
    },
    "ALONGADO": {
        "MASCULINO": {"MEDIO": {"corte": "Side Part com Laterais Cheias", "descricao": "Mantém densidade lateral."}},
        "FEMININO": {"MEDIO": {"corte": "Chanel na Altura do Queixo", "descricao": "Encurta o rosto com elegância."}},
        "AFRO": {"MEDIO": {"corte": "Black Power Horizontalizado", "descricao": "Mais largo que alto."}},
        "INFANTIL": {"MEDIO": {"corte": "Chanel Clássico", "descricao": "Proporcional e harmonioso."}},
        "TERCEIRA_IDADE": {"MEDIO": {"corte": "Bob com Franja Desfiada", "descricao": "Suaviza os traços."}}
    }
}

def consultar_estilo(formato_rosto, perfil, idade=None, comprimento="MEDIO"):
    """
    Busca o estilo baseado no formato, perfil, idade e comprimento,
    sincronizando o resultado com a memória comum 🧠.
    """
    formato = formato_rosto.upper() if formato_rosto else "OVAL"
    perfil_key = perfil.upper() if perfil else "MASCULINO"
    
    # Lógica de Terceira Idade (40+)
    if idade and isinstance(idade, (int, float)) and idade >= 40:
        perfil_key = "TERCEIRA_IDADE"
        
    rosto_data = MATRIZ_ESTILO.get(formato, MATRIZ_ESTILO["OVAL"])
    perfil_data = rosto_data.get(perfil_key, rosto_data.get("MASCULINO", {}))
    
    resultado = perfil_data.get(comprimento.upper(), perfil_data.get("MEDIO", {
        "corte": "Estilo Executivo",
        "descricao": "Harmonização universal."
    }))
    
    # 🔗 Salvando o resultado na memória comum para o orquestrador acessar
    try:
        memoria.salvar_dados("ultima_consulta_estilo", {
            "formato": formato,
            "perfil": perfil_key,
            "idade": idade,
            "comprimento": comprimento,
            "resultado": resultado
        })
    except Exception:
        pass
        
    return resultado

def processar(dados_entrada=None):
    """Função de compatibilidade para chamada direta via orquestrador 💻."""
    if dados_entrada and isinstance(dados_entrada, dict):
        formato = dados_entrada.get("formato_rosto", "OVAL")
        perfil = dados_entrada.get("perfil", "MASCULINO")
        idade = dados_entrada.get("idade")
        comprimento = dados_entrada.get("comprimento", "MEDIO")
        return consultar_estilo(formato, perfil, idade, comprimento)
    return {"status": "Módulo de Estilos pronto para uso"}

if __name__ == "__main__":
    print(processar({"formato_rosto": "QUADRADO", "perfil": "FEMININO", "idade": 35, "comprimento": "MEDIO"}))