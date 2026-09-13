from security.input_sanitizer import InputSanitizer

def testar_seguranca():
    # Exemplos de entradas perigosas que um atacante tentaria
    entradas_suspeitas = [
        "thierry'; DROP TABLE usuarios;--",  # SQL Injection clássico
        "<script>alert('hack');</script>",    # XSS Attack
        "SELECT * FROM dados_secretos",        # Tentativa de consulta não autorizada
        "Usuário Legítimo 2026"                # Entrada esperada
    ]
    
    print("--- INICIANDO TESTE DE SANITIZAÇÃO DE INPUT ---")
    print("Aguarde a limpeza dos dados...\n")
    
    for entrada in entradas_suspeitas:
        # Chamando o método correto que você definiu: limpar_string
        limpo = InputSanitizer.limpar_string(entrada)
        
        print(f"ENTRADA ORIGINAL: {entrada}")
        print(f"DADO SANITIZADO:  {limpo}")
        print("-" * 40)

if __name__ == "__main__":
    testar_seguranca()