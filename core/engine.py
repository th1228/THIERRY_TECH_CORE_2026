import asyncio
import logging
import sys
import cv2
import mediapipe as mp
import time
from typing import Dict, Any

# Importação segura do seu módulo de métricas
try:
    import metrics
except ImportError:
    logging.error("O arquivo 'metrics.py' não foi encontrado no mesmo diretório.")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Inicialização das ferramentas de Malha Facial do MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# ESTÉTICA DE ELITE (AZUL CYAN NEON)
NEON_CYAN_COLOR = (255, 255, 0) 

custom_tesselation_style = mp_drawing.DrawingSpec(
    color=NEON_CYAN_COLOR, 
    thickness=1, 
    circle_radius=1
)

custom_contour_style = mp_drawing.DrawingSpec(
    color=NEON_CYAN_COLOR, 
    thickness=2, 
    circle_radius=1
)

async def process_camera_stream():
    """Abre a câmera, renderiza a malha facial neon de alta precisão e processa dados."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.critical("Não foi possível acessar a webcam.")
        return

    logging.info("Core de Visão Ativado. Estética Neon carregada.")
    logging.info("Controles no teclado: [S] Salvar Foto | [Q] Sair do Programa")

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                await asyncio.sleep(0.1)
                continue

            # Efeito espelho natural
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            real_facial_data = {}

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    
                    # Desenha a malha interna
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=custom_tesselation_style
                    )
                    
                    # Desenha os contornos de expressão
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=custom_contour_style
                    )

                    try:
                        ponto_testa = face_landmarks.landmark[10]
                        ponto_queixo = face_landmarks.landmark[152]
                        ponto_olho_esquerdo = face_landmarks.landmark[33]
                        ponto_olho_direito = face_landmarks.landmark[263]

                        face_height = abs(ponto_testa.y - ponto_queixo.y) * h
                        face_width = abs(ponto_olho_esquerdo.x - ponto_olho_direito.x) * w

                        real_facial_data = {
                            "face_height_px": round(face_height, 2),
                            "face_width_px": round(face_width, 2),
                            "asymmetry_ratio": round(abs(face_height / (face_width if face_width > 0 else 1)), 4)
                        }

                        if hasattr(metrics, 'calculate_visagism_metrics'):
                            processed = metrics.calculate_visagism_metrics(real_facial_data)
                            status_text = f"Analise: {processed.get('status', 'Processando')}"
                        else:
                            status_text = "Dados extraídos com sucesso!"

                        cv2.putText(frame, "TTC GLOBAL CORE - MALHA NEON ATIVA", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, NEON_CYAN_COLOR, 2)
                        cv2.putText(frame, status_text, (10, 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                    except Exception:
                        pass
            else:
                cv2.putText(frame, "Procurando Rosto...", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.putText(frame, "Comandos: [S] Salvar Imagem | [Q] Sair", (10, h - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            # LINHA CORRIGIDA COM PARÊNTESES FECHADOS PERFEITAMENTE:
            cv2.imshow("TTC Global Engine - Facial Scanning", frame)

            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s') or key == ord('S'):
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"captura_facial_{timestamp}.png"
                cv2.imwrite(filename, frame)
                logging.info(f"CAPTURA SALVA: {filename}")
                
                cv2.putText(frame, "FOTO SALVA!", (int(w/2) - 100, int(h/2)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                cv2.imshow("TTC Global Engine - Facial Scanning", frame)
                cv2.waitKey(400)

            elif key == ord('q') or key == ord('Q'):
                break
                
            await asyncio.sleep(0.001)

        cap.release()
        cv2.destroyAllWindows()

async def main():
    try:
        logging.info("--- Inicializando Core de Visão Computacional Nível 1 ---")
        await process_camera_stream()
    except Exception as e:
        logging.critical(f"Erro inesperado no sistema: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())