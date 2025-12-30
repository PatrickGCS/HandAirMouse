import cv2
import pyautogui
import math
import numpy as np
import time

# --- IMPORTAÇÃO SEGURA DO MEDIAPIPE ---
import mediapipe as mp
try:
    from mediapipe.python.solutions import hands as mp_hands_solution
    from mediapipe.python.solutions import drawing_utils as mp_draw_solution
except ImportError:
    import mediapipe.solutions.hands as mp_hands_solution
    import mediapipe.solutions.drawing_utils as mp_draw_solution

# --- CONFIGURAÇÕES ---
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

wCam, hCam = 640, 480
wTela, hTela = pyautogui.size()
frame_reduction = 100 
smoothening = 4  # Suavização (aumente se tremer)

# Variáveis globais
plocX, plocY = 0, 0 
clocX, clocY = 0, 0 
dist_anterior_maos = None 
pTime = 0

# --- INICIALIZAÇÃO DA CÂMARA (Verifique se é 0, 1 ou 2) ---
cap = cv2.VideoCapture(1) # <--- CONFIRA SE O SEU ÍNDICE AINDA É 1

# Ajuste de sensibilidade: Detection mais baixo ajuda a encontrar a mão
# Tracking mais alto ajuda a não perder o dedo
hands = mp_hands_solution.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.7 
)
mp_draw = mp_draw_solution

print("Sistema Melhorado. Pressione 'q' para sair.")

while True:
    success, img = cap.read()
    if not success:
        cv2.waitKey(10)
        continue

    img = cv2.resize(img, (wCam, hCam))
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    lmList = []
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands_solution.HAND_CONNECTIONS)
            
            myHand = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                myHand.append([id, cx, cy])
            lmList.append(myHand)

    if len(lmList) > 0:
        # --- LÓGICA DE UMA MÃO (Rato) ---
        if len(lmList) == 1:
            dist_anterior_maos = None
            hand = lmList[0]
            
            # Pontos principais
            x1, y1 = hand[8][1], hand[8][2]   # Ponta do Indicador
            x2, y2 = hand[12][1], hand[12][2] # Ponta do Médio
            x_polegar, y_polegar = hand[4][1], hand[4][2] # Ponta do Polegar
            
            # --- NOVA LÓGICA DE DETEÇÃO DE DEDOS ---
            # Em vez de comparar com a junta de cima, comparamos com a base (knuckle)
            # Isso evita erros quando o dedo está inclinado.
            fingers = []
            
            # Polegar (lógica lateral - depende da mão direita/esquerda, simplificado aqui)
            if hand[4][1] < hand[3][1]: fingers.append(1)
            else: fingers.append(0)
            
            # Indicador (Compara ponta [8] com a base [5])
            if hand[8][2] < hand[5][2]: fingers.append(1) 
            else: fingers.append(0)
            
            # Médio (Compara ponta [12] com a base [9])
            if hand[12][2] < hand[9][2]: fingers.append(1)
            else: fingers.append(0)
            
            # Anelar (Compara ponta [16] com a base [13])
            if hand[16][2] < hand[13][2]: fingers.append(1)
            else: fingers.append(0)
            
            # Mindinho (Compara ponta [20] com a base [17])
            if hand[20][2] < hand[17][2]: fingers.append(1)
            else: fingers.append(0)

            # Contagem de dedos levantados (sem o polegar)
            upCount = fingers[1:].count(1)
            estado_texto = "PARADO"

            # 1. MOVER: Apenas Indicador levantado (Médio ABAIXO da base)
            # Adicionada verificação extra: O dedo médio TEM de estar dobrado
            if fingers[1] == 1 and fingers[2] == 0:
                estado_texto = "MOVER"
                
                # Desenha Área Ativa
                cv2.rectangle(img, (frame_reduction, frame_reduction), 
                             (wCam - frame_reduction, hCam - frame_reduction), (255, 0, 255), 2)
                
                # Círculo verde grande no indicador
                cv2.circle(img, (x1, y1), 20, (0, 255, 0), cv2.FILLED)
                
                # Conversão de coordenadas
                convX = np.interp(x1, (frame_reduction, wCam - frame_reduction), (0, wTela))
                convY = np.interp(y1, (frame_reduction, hCam - frame_reduction), (0, hTela))
                
                # Suavização
                clocX = plocX + (convX - plocX) / smoothening
                clocY = plocY + (convY - plocY) / smoothening
                
                try:
                    pyautogui.moveTo(clocX, clocY)
                except:
                    pass
                plocX, plocY = clocX, clocY

            # 2. CLIQUE (Pinça) - Funciona independente se o indicador está "em pé" ou não
            dist_pinca = math.hypot(x1 - x_polegar, y1 - y_polegar)
            if dist_pinca < 45: # Aumentei um pouco a distância de deteção
                estado_texto = "CLIQUE"
                cv2.circle(img, (x1, y1), 20, (0, 0, 255), cv2.FILLED)
                if fingers[1] == 1: # Só clica se o indicador estiver ativo
                    pyautogui.click()

            # 3. SCROLL
            if fingers[1] == 1 and fingers[2] == 1:
                if fingers[3] == 1: # 3 dedos
                    estado_texto = "SCROLL UP"
                    pyautogui.scroll(120)
                else: # 2 dedos
                    estado_texto = "SCROLL DOWN"
                    pyautogui.scroll(-120)
            
            # 4. BOTÃO DIREITO
            if upCount == 4:
                estado_texto = "DIREITO"
                pyautogui.rightClick()
                time.sleep(0.3)

            # Mostra o estado na tela
            cv2.putText(img, f"Estado: {estado_texto}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

        # --- LÓGICA DE DUAS MÃOS (Zoom) ---
        elif len(lmList) == 2:
            mao1_x, mao1_y = lmList[0][0][1], lmList[0][0][2]
            mao2_x, mao2_y = lmList[1][0][1], lmList[1][0][2]
            dist_atual = math.hypot(mao2_x - mao1_x, mao2_y - mao1_y)
            
            cv2.line(img, (mao1_x, mao1_y), (mao2_x, mao2_y), (255, 255, 0), 3)
            cv2.putText(img, "ZOOM", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

            if dist_anterior_maos is not None:
                if dist_atual > dist_anterior_maos + 6:
                    pyautogui.hotkey('ctrl', '+')
                elif dist_atual < dist_anterior_maos - 6:
                    pyautogui.hotkey('ctrl', '-')
            dist_anterior_maos = dist_atual

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, hCam - 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Controle de Rato AI", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()