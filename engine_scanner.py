import cv2
import mediapipe as mp
import threading

def rodar_camera():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        # Processamento leve do MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        # O resultado aparece apenas no terminal para não dar conflito visual
        if results.multi_face_landmarks:
            print("Scanner Ativo: Rosto detectado com sucesso.")
            
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()

def iniciar_scanner_thread():
    # Isso inicia a câmera sem travar o seu layout All Black
    t = threading.Thread(target=rodar_camera, daemon=True)
    t.start()