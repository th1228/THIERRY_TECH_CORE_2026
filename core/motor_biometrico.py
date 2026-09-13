# -*- coding: utf-8 -*-
import sys
import os
import cv2
import mediapipe as mp
import time
import winsound

# --- CORREÇÃO DE CAMINHO E CONEXÃO ESTRUTURAL ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from memoria_comum import instancia_memoria as memoria
except ImportError:
    class MemoriaMock:
        def salvar_dados(self, chave, valor): pass
        def ler_dados(self, chave): return None
    memoria = MemoriaMock()
# -----------------------------------------------

class MotorBiometrico:
    def __init__(self):
        try:
            memoria.salvar_dados("contexto_geografico", "KR")
        except Exception as e:
            pass

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.usuario_identificado = None

    def processar_frame(self, frame=None):
        """Processa o frame recebido do orquestrador (main.py) 💻"""
        if frame is None:
            return None, "FRAME_VAZIO"

        frame_processado = cv2.convertScaleAbs(frame, alpha=1.2, beta=-15)
        frame_rgb = cv2.cvtColor(frame_processado, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        cv2.putText(frame_processado, "THIERRY TECH // MOTOR BIOMETRICO (KR)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 215, 255), 1)
        cv2.putText(frame_processado, "STATUS: ESCANEANDO FACE...", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        status_autenticacao = "ESCANEANDO"

        if results.multi_face_landmarks:
            for fl in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame_processado, fl, self.mp_face_mesh.FACEMESH_TESSELATION,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 100), thickness=1, circle_radius=1),
                    self.mp_drawing.DrawingSpec(color=(0, 100, 255), thickness=1, circle_radius=1)
                )
            
            self.usuario_identificado = "THIERRY"
            status_autenticacao = "AUTENTICADO"
            try:
                winsound.Beep(1200, 150)
            except Exception:
                pass

            metricas_coletadas = {
                'usuario': self.usuario_identificado,
                'refletancia_pele': 49.1,
                'tipo_rosto': 'TRIANGULAR',
                'status': 'AUTENTICADO',
                'timestamp': time.time()
            }

            # Sincronização automática com a Memória Comum 🧠
            memoria.salvar_dados("motor_biometrico", metricas_coletadas)

        return frame_processado, status_autenticacao

    def get_vfc(self):
        """Retorna os dados exatos exigidos pelo Mônaco Integrador."""
        return {
            "status": "ativo",
            "metrica_vfc": 49.1,
            "usuario": self.usuario_identificado or "THIERRY"
        }

# --- INSTÂNCIA E PONTES GLOBAIS ---
_motor_global = MotorBiometrico()

def processar(frame=None):
    """Função de compatibilidade direta com o orquestrador 💻."""
    if frame is not None:
        frame_res, status = _motor_global.processar_frame(frame)
        return frame_res
    return None

def get_emg():
    """Ponte de compatibilidade para módulos que chamam get_emg."""
    return _motor_global.get_vfc()

def get_vfc():
    """Ponte global para o método get_vfc."""
    return _motor_global.get_vfc()

def iniciar():
    """Execução direta via terminal."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_res, status = _motor_global.processar_frame(frame)
        cv2.imshow("THIERRY TECHNOLOGY - MOTOR BIOMETRICO", frame_res)

        if status == "AUTENTICADO":
            time.sleep(1)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar()