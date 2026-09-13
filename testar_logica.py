# -*- coding: utf-8 -*-
from core.biometria import obter_laudo_biometrico

def testar_fluxo_logico():
    print("=" * 65)
    print(" THIERRY TECH CORE — TESTE DE LÓGICA DE BIOMETRIA")
    print("=" * 65)
    
    # Executa o cálculo antropométrico e gera o laudo
    laudo_teste = obter_laudo_biometrico(
        testa=14.0, 
        macas=15.5, 
        mandibula=12.5, 
        altura=22.0, 
        genero="masculino", 
        clima="tropical"
    )
    
    for chave, valor in laudo_teste.items():
        print(f"[{chave}]: {valor}")
    
    print("=" * 65)
    print(" Status: Módulo rodando com sucesso e integração limpa!")
    print("=" * 65)

if __name__ == "__main__":
    testar_fluxo_logico()