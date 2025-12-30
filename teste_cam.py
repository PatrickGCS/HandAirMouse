import cv2

print("Procurando câmeras ativas...")

# Testa os primeiros 5 índices possíveis
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"[SUCESSO] Câmera encontrada no índice: {i}")
            print(f"Resolução: {frame.shape[1]}x{frame.shape[0]}")
            # Tenta mostrar a imagem rapidinho para você ver se é a do celular
            cv2.imshow(f'Camera {i}', frame)
            cv2.waitKey(1000) 
            cv2.destroyAllWindows()
        else:
            print(f"[FALHA] Índice {i} abre, mas não retorna imagem (Tela preta/Iriun desconectado?)")
    else:
        print(f"[VAZIO] Nenhuma câmera no índice {i}")
    cap.release()