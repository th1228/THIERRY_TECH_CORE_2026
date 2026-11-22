import os

# Aqui definimos os ficheiros separados e o conteúdo real que cada um vai ter
# Podes alterar os nomes e o conteúdo de acordo com o que precisas no teu sistema.
documentos_e_modulos = {
    
    # Módulo para o Backend/Servidor (Ex: FastAPI)
    "servidor_backend.py": '''# ==========================================
# MÓDULO DE SERVIDOR BACKEND (FastAPI / Rotas)
# ==========================================
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Soberano Kernel Ativo", "porta": 801}
''',

    # Módulo para Lógica de Relatórios / PDF
    "gerador_relatorios.py": '''# ==========================================
# MÓDULO DE COMPILAÇÃO E RELATÓRIOS PDF
# ==========================================
def compilar_dossiie(tipo, cliente):
    print(f"[PDF] A gerar dossiê do tipo '{tipo}' para a entidade: {cliente}")
    # Insere aqui a lógica de geração de PDF
''',

    # Documentação / Notas Técnicas do Projeto
    "documentacao_tecnica.md": '''# Documentação Oficial do Sistema
    
- **Arquitetura:** Monaco Tier-1 Audit Terminal
- **Porta de Comunicação:** 801
- **Estado:** Modularizado e Organizado com Sucesso.
'''
}

def criar_estrutura_modular():
    # Cria uma pasta segura chamada 'modulos_organizados' para guardar os novos ficheiros
    pasta_destino = "modulos_organizados"
    os.makedirs(pasta_destino, exist_ok=True)
    
    print(f"[INÍCIO] A criar a estrutura na pasta '{pasta_destino}'...\n")
    
    criados = 0
    for nome_ficheiro, conteudo in documentos_e_modulos.items():
        caminho_completo = os.path.join(pasta_destino, nome_ficheiro)
        try:
            with open(caminho_completo, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"[CRIADO COM SUCESSO] -> {caminho_completo}")
            criados += 1
        except Exception as e:
            print(f"[ERRO] Falha ao criar {nome_ficheiro}: {e}")
            
    print(f"\n[CONCLUÍDO] Foram gerados {criados} ficheiros separados com sucesso!")

if __name__ == "__main__":
    criar_estrutura_modular()