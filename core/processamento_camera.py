# processamento_câmera.py
import cv2
import mediapipe as mp
import motor_dados # O novo arquivo central que vamos criar

def rodar_scanner():
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Driver fixo para não perder a câmera
    
    print("[SCANNER] Sistema de Alta Precisão Ativo...")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success: continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            # Aqui você desenha a malha neon
            for face_landmarks in results.multi_face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 204), thickness=1))

        cv2.imshow('TTC - Cybernetic Scan Engine', frame)
        
        # Gatilho de Captura
        if cv2.waitKey(5) & 0xFF == ord('s'):
            # AQUI: CALCULAMOS OS DADOS E SALVAMOS NO MOTOR
            dados_capturados = {"status": "Escaneado", "timestamp": "2026-06-10"}
            motor_dados.salvar("scanner", dados_capturados)
            print("[SCANNER] Dados salvos no Motor de Dados.")
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    rodar_scanner()