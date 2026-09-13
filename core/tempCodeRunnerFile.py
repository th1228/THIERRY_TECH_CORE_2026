_atual = frame.copy()

            if not modo_web:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27: break

        cap.release()
        if not modo_web: cv2.destroyAllWindows()