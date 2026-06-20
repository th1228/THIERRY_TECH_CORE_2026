import requests

def checar_licenca_na_nuvem(chave):
    try:
        # A URL abaixo será o seu servidor no futuro
        # Por enquanto, estamos apenas preparando o código
        url_do_servidor = "https://sua-nuvem-de-seguranca.com/validar"
        
        # Envia a chave para o servidor verificar
        resposta = requests.post(url_do_servidor, data={'chave': chave}, timeout=5)
        
        if resposta.status_code == 200:
            return resposta.text == "VALIDO"
        return False
        
    except Exception:
        # Se a internet cair ou o servidor estiver offline, o sistema é bloqueado
        # Isso é segurança defensiva!
        return False

# Agora, no seu gui_main.py, você simplesmente chama:
# if checar_licenca_na_nuvem(chave_digitada):
#     abrir_programa()