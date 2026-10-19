import os
import re

def auditar_geradores():
    print("=" * 60)
    print("   TCC GLOBAL • AUDITORIA DE GERADORES DE PDF")
    print("=" * 60)
    print(f"Diretório atual: {os.getcwd()}\n")
    
    arquivos = [f for f in os.listdir('.') if f.endswith('.py')]
    encontrados = 0
    
    for arquivo in arquivos:
        if arquivo == "auditar_geradores_pdf.py":
            continue
            
        try:
            with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                conteudo = f.read()
                
            termo_pdf = 'pdf' in conteudo.lower()
            termo_reportlab = 'reportlab' in conteudo.lower()
            termo_gerador = 'gerar' in conteudo.lower() or 'build' in conteudo.lower()
            
            if termo_pdf or termo_reportlab or termo_gerador:
                encontrados += 1
                print(f"📄 Arquivo Identificado: {arquivo}")
                
                funcoes = re.findall(r'def\s+(\w+)\s*\(', conteudo)
                if funcoes:
                    print(f"   ⚙️ Funções: {', '.join(funcoes)}")
                    
                chaves = re.findall(r'["\'](modelo_matematico|lideranca|visagismo|monaco|roi|pitch|governanca|clinica)["\']', conteudo, re.IGNORECASE)
                if chaves:
                    print(f"   🎯 Alvos detectados: {list(set(chaves))}")
                    
                print("-" * 60)
        except Exception as e:
            print(f"⚠️ Erro ao ler o arquivo {arquivo}: {e}")
            
    if encontrados == 0:
        print("Nenhum script com indícios de PDF foi encontrado neste diretório.")
    else:
        print(f"\nTotal de arquivos encontrados: {encontrados}")

if __name__ == "__main__":
    auditar_geradores()