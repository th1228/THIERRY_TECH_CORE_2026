import platform
import uuid
import math

def obter_fingerprint_hardware():
    """Gera uma assinatura única e infalsificável baseada no hardware da máquina."""
    node = uuid.getnode()
    sistema = platform.system()
    maquina = platform.node()
    # Combina componentes estáticos do computador
    fingerprint_base = f"{node}-{sistema}-{maquina}"
    return fingerprint_base

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """Calcula a distância em quilômetros usando a fórmula de Haversine."""
    R = 6371.0  # Raio médio da Terra em km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def soberign_gate_validador(lat_atual, lon_atual, lat_base, lon_base, hash_hardware_autorizado):
    """Executa a checagem dupla: Hardware + Raio Territorial de 100 km."""
    
    print("[*] SOVEREIGN GATE: Iniciando varredura de integridade e perímetro...")

    # Camada A: Validação de Hardware (Máquina única)
    hardware_atual = obter_fingerprint_hardware()
    if hardware_atual != hash_hardware_autorizado:
        print("[X] FALHA CRÍTICA: Assinatura de hardware incompatível. Acesso negado.")
        return False
    print("[✓] Hardware validado com sucesso.")

    # Camada B: Validação de Domínio Territorial (Geofence de 100 km)
    distancia_km = calcular_distancia_km(lat_atual, lon_atual, lat_base, lon_base)
    print(f"[i] Distância calculada do domínio central: {distancia_km:.2f} km")

    LIMITE_TERRITORIAL_KM = 100.0

    if distancia_km <= LIMITE_TERRITORIAL_KM:
        print("[✓] Perímetro Territorial OK: Dentro do limite de 100 km.")
        return True
    else:
        print(f"[X] FALHA CRÍTICA: Fora do domínio autorizado ({distancia_km:.2f} km > 100 km). Acesso bloqueado.")
        return False

if __name__ == "__main__":
    # Exemplo de uso:
    # 1. Defina as coordenadas da base (ex: São Luís / MA)
    LAT_SEDE = -2.53073
    LON_SEDE = -44.30680

    # 2. Defina o hash do hardware autorizado (você pode gerar uma vez na sua máquina e salvar no config)
    MEU_HARDWARE_HASH = obter_fingerprint_hardware() 

    # Simulação de teste com a localização atual dentro do limite de 100 km
    permissao_concedida = soberign_gate_validador(
        lat_atual=-2.54000, 
        lon_atual=-44.31000, 
        lat_base=LAT_SEDE, 
        lon_base=LON_SEDE, 
        hash_hardware_autorizado=MEU_HARDWARE_HASH
    )
    
    if permissao_concedida:
        print("\n[STATUS] Sistema liberado para operação.")
    else:
        print("\n[STATUS] Sistema travado por violação de segurança.")