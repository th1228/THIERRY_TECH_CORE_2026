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
    "OVAL": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}},
    "REDONDO": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}},
    "QUADRADO": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}},
    "CORACAO": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}},
    "TRIANGULAR": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}},
    "DIAMANTE": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}},
    "ALONGADO": {"MASCULINO": {}, "FEMININO": {}, "AFRO": {}, "INFANTIL": {}, "TERCEIRA_IDADE": {}}
}

def consultar_estilo(formato_rosto, perfil, idade=None, comprimento="MEDIO"):
    """
    Busca o estilo baseado no formato, perfil, idade e comprimento,
    sincronizando o resultado com a memória comum 🧠.
    """
    formato = formato_rosto.upper()
    perfil_key = perfil.upper()
    
    # Lógica de Terceira Idade (40+)
    if idade and idade >= 40:
        perfil_key = "TERCEIRA_IDADE"
        
    rosto_data = MATRIZ_ESTILO.get(formato, MATRIZ_ESTILO["OVAL"])
    perfil_data = rosto_data.get(perfil_key, rosto_data["MASCULINO"])
    
    resultado = perfil_data.get(comprimento.upper(), perfil_data.get("MEDIO", {}))
    
    # 🔗 Salvando o resultado na memória comum para o main.py acessar
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
    """Função de compatibilidade para chamada direta via main.py 💻."""
    if dados_entrada and isinstance(dados_entrada, dict):
        formato = dados_entrada.get("formato_rosto", "OVAL")
        perfil = dados_entrada.get("perfil", "MASCULINO")
        idade = dados_entrada.get("idade")
        comprimento = dados_entrada.get("comprimento", "MEDIO")
        return consultar_estilo(formato, perfil, idade, comprimento)
    return {"status": "Módulo de Estilos pronto para uso"}