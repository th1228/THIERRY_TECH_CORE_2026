import cv2
import mediapipe as mp
import time
import winsound
import numpy as np

# Configuração da Malha
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)

def main():
    camera = cv2.VideoCapture(0)
    estado = "INICIAR"
    inicio_timer = 0
    scan_y = 0 

    while True:
        ret, frame = camera.read()
        if not ret: break

        # --- EFEITO: SCANNER DINÂMICO ---
        # scan_y é a linha invisível que desce
        scan_y = (scan_y + 8) % frame.shape[0]
        
        # Processamento Facial
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for lm in face_landmarks.landmark:
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    # Distância do ponto atual para a linha do scanner
                    dist = abs(cy - scan_y)
                    
                    # Lógica de brilho/tamanho: quanto mais perto da linha, maior o ponto
                    # Se estiver a menos de 50 pixels da linha, o ponto cresce
                    if dist < 50:
                        size = int(4 - (dist / 15)) # O ponto varia de tamanho
                        color = (255, 255, 255) # Branco no centro do feixe
                    else:
                        size = 1
                        color = (255, 255, 0) # Ciano padrão
                        
                    cv2.circle(frame, (cx, cy), size, color, -1)

        # Interface Pequena (mantida conforme pedido)
        cv2.putText(frame, f"STATUS: {estado}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        # Máquina de Estados (lógica de captura mantida)
        if estado == "INICIAR":
            cv2.putText(frame, "PRESSIONE 'I' PARA INICIAR", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            if cv2.waitKey(1) & 0xFF == ord('i'):
                estado = "RESPIRAÇÃO"
                inicio_timer = time.time()
        
        elif estado == "RESPIRAÇÃO":
            tempo = int(time.time() - inicio_timer)
            cv2.putText(frame, f"ANALISANDO: {tempo}s", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            if tempo >= 10: estado = "ESPERA"

        elif estado == "ESPERA":
            cv2.putText(frame, "OK! PRESSIONE 'S' PARA CAPTURAR", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                # Flash
                flash = np.ones(frame.shape, dtype=np.uint8) * 255
                cv2.imshow("THIERRY BIOGEMIO DIGITAL", flash)
                winsound.Beep(1500, 200)
                cv2.waitKey(200)
                cv2.imwrite("resultado_biometria.jpg", frame)
                estado = "FIM"

        cv2.imshow("THIERRY BIOGEMIO DIGITAL", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()