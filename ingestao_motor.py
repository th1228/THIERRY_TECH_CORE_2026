# -*- coding: utf-8 -*-
import os
from typing import Any
import cv2


def alimentar_motor_com_imagem(
    caminho_foto: str,
    processar_frame_biometrico: Any,
    memoria_global: Any,
) -> dict[str, Any]:
    """Carrega uma imagem frontal nítida, executa o motor local e grava em memoria_global."""
    if not os.path.exists(caminho_foto):
        raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho_foto}")

    frame = cv2.imread(caminho_foto)
    if frame is None:
        raise FileNotFoundError(f"Não foi possível decodificar a imagem: {caminho_foto}")

    resultado_motor = processar_frame_biometrico(frame)

    if not resultado_motor or not resultado_motor.get("face_detectada"):
        raise RuntimeError("Nenhum rosto foi detectado na imagem fornecida.")

    if hasattr(memoria_global, "salvar_dados"):
        memoria_global.salvar_dados("motor_biometrico_atual", resultado_motor)
    elif isinstance(memoria_global, dict):
        memoria_global["motor_biometrico_atual"] = resultado_motor
    else:
        raise TypeError("memoria_global incompatível: esperado dict ou objeto com salvar_dados().")

    phi = float(resultado_motor.get("phi_global") or 0.0)
    proj = resultado_motor.get("projecoes_anos") or {}
    print(f"[OK] Motor processado! Phi: {phi:.3f}")
    print(f"[OK] Projeções carregadas: {list(proj.keys())}")
    return resultado_motor


if __name__ == "__main__":
    # Ajuste o nome do módulo abaixo caso seu motor ou memoria_global estejam em outro arquivo
    from core.memoria_comum import memoria_global
    from motor_biometrico import processar_frame_biometrico

    caminho_foto = "teste_rosto.jpg"
    alimentar_motor_com_imagem(caminho_foto, processar_frame_biometrico, memoria_global)