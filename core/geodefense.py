import math
import uuid


def calcular_distancia_km(lat1, lon1, lat2, lon2):
  # Fórmula de Haversine para cálculo preciso de distância entre coordenadas globais
  R = 6371.0  # Raio da Terra em km
  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)
  a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
      math.radians(lat2)
  ) * math.sin(dlon / 2) ** 2
  c = 2 * math.asin(math.sqrt(a))
  return R * c


def gerar_token_titular_global():
  return f"TTC-GLOBAL-{uuid.uuid4().hex[:8].upper()}"


def validar_geofencing_global(
    nova_lat, nova_lon, token_titular_atual, base_licencas_ativas
):
  RAIO_LIMITE_KM = 100.0

  for licenca in base_licencas_ativas:
    distancia = calcular_distancia_km(
        nova_lat, nova_lon, licenca["lat"], licenca["lon"]
    )

    if distancia < RAIO_LIMITE_KM:
      if licenca["tenant_id"] == token_titular_atual:
        print(
            f"[AUTORIZADO GLOBAL] Expansão multiloja permitida para o titular"
            f" {token_titular_atual} (Distância: {round(distancia, 2)} km)."
        )
        return True
      else:
        print(
            f"[BLOQUEIO GLOBAL] Conflito territorial: Raio de 100km violado."
            f" Unidade pertencente a outro titular global."
        )
        return False

  print(
      "[AUTORIZADO GLOBAL] Nova licença fora do perímetro restrito. Posição"
      " aprovada."
  )
  return True