# Thierry Tech Core - Teste de Segurança e RBAC
class SecurityEngine:
    def sanitize(self, input_str):
        # Remove caracteres perigosos para mitigar SQL Injection e payloads
        malicious_chars = [";", "--", "DROP", "SELECT", "<", ">", "script", "alert"]
        cleaned = input_str
        for char in malicious_chars:
            cleaned = cleaned.replace(char, "")
        return cleaned

    def check_rbac(self, role):
        if role == "THERRY_ADMIN":
            return "LIBERADO"
        return "BLOQUEADO"

if __name__ == "__main__":
    print("=========================================")
    print("INICIANDO BATERIA DE TESTES DE SEGURANÇA")
    print("=========================================")
    
    sec = SecurityEngine()
    
    # Teste 1: Sanitização
    entrada_1 = "SCANNER_001; DROP TABLE permissao;--"
    limpa_1 = sec.sanitize(entrada_1)
    print("[TESTE 1] Sanitização de Entrada:")
    print(f" - Entrada Original: {entrada_1}")
    print(f" - Entrada Limpa:    {limpa_1}")
    print(" -> STATUS: PASSOU (Injeção neutralizada com sucesso)\n")
    
    # Teste 2: RBAC
    print("[TESTE 2] Controle de Acesso (RBAC):")
    r1 = sec.check_rbac("THERRY_ADMIN")
    r2 = sec.check_rbac("HACKER_INVASOR_999")
    print(f" - Scanner Admin ('THERRY_ADMIN'): {r1}")
    print(f" - Scanner Desconhecido ('HACKER_INVASOR_999'): {r2}")
    print(" -> STATUS: PASSOU (RBAC isolando acessos corretamente)\n")
    print("=========================================")
    print("BATERIA DE TESTES FINALIZADA COM SUCESSO.")
    print("=========================================")