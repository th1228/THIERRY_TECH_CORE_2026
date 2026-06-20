import cv2
import sys

# Garante que o Python feche tudo se você interromper
def iniciar_dual_scan_total():
    # 1. Fecha janelas fantasmas
    cv2.destroyAllWindows()
    
    # 2. Liga as câmeras 0 e 1 usando o modo DirectShow (mais estável)
    print("Conectando as cameras do sistema TTC...")
    cam0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cam0.isOpened() or not cam1.isOpened():
        print("Aviso: Uma das cameras esta ocupada. Feche outros programas!")
        return

    print("SISTEMA ON-LINE! Pressione 'q' no teclado para sair.")

    while True:
        ret0, frame0 = cam0.read()
        ret1, frame1 = cam1.read()

        if ret0:
            cv2.imshow("SCAN 01 - FRONTAL", frame0)
        if ret1:
            cv2.imshow("SCAN 02 - LATERAL", frame1)

        # Se apertar 'q', o programa solta as câmeras para o Windows
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 3. Liberação obrigatória - Isso evita o erro de 'carregando' na próxima vez
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()
    print("Cameras liberadas com sucesso.")

if __name__ == "__main__":
    iniciar_dual_scan_total()