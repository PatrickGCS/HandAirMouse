# 🖱️ Hand Air Mouse (AI Gesture Control)

Ferramenta de controlo de mouse via webcam utilizando Visão Computacional e Inteligência Artificial. Este projeto permite mover o cursor, clicar, fazer scroll e dar zoom utilizando apenas gestos das mãos, sem necessidade de hardware extra além de uma câmara (ou telemóvel via Iriun Webcam).

## 🚀 Funcionalidades

O sistema reconhece gestos específicos para realizar ações no Windows:


| Gesto                               | Ação              | Descrição Visual                                                     |
| ------------------------------------- | --------------------- | ------------------------------------------------------------------------ |
| **👆 Indicador Levantado**          | **Mover Mouse**      | Mantenha apenas o indicador levantado. O cursor segue a ponta do dedo. |
| **🤏 Pinça (Indicador + Polegar)** | **Clique Esquerdo** | Aproxime a ponta do polegar com a ponta do indicador (toque rápido).  |
| **✌️ Dois Dedos (V)**             | **Scroll Down**     | Levante o indicador e o dedo médio.                                   |
| **🤟 Três Dedos**                  | **Scroll Up**       | Levante indicador, médio e anelar.                                    |
| **✋ Mão Aberta**                  | **Clique Direito**  | Levante 4 ou 5 dedos.                                                  |
| **👐 Duas Mãos (Afastar/Juntar)**  | **Zoom (Ctrl +/-)** | Junte as palmas para diminuir o zoom, afaste para aumentar.            |

## 🛠️ Pré-requisitos e Instalação

Devido a conflitos conhecidos entre o **Numpy 2.0** e o **MediaPipe** no Windows, é **crítico** instalar as versões específicas listadas abaixo para garantir o funcionamento e evitar erros de atributos.

### 1. Preparação

Certifique-se de que tem o Python instalado (recomendado 3.10 ou 3.11).

### 2. Instalar Dependências (Versões Estáveis)

Abra o terminal na pasta do projeto e execute o comando abaixo para instalar o "combo estável":

```
pip install numpy==1.26.4 opencv-python==4.9.0.80 mediapipe==0.10.9 protobuf==3.20.3 pyautogui
```

> **Nota:** O uso do `protobuf==3.20.3` e `numpy==1.26.4` é obrigatório para evitar o erro `AttributeError: module 'mediapipe' has no attribute 'solutions'`.

## 💻 Como Usar

1. **Conecte a sua Câmara:**
   * Se estiver a usar **Iriun Webcam** , certifique-se de que a aplicação está aberta no telemóvel e no PC.
   * *Recomendação:* Use conexão via **Cabo USB** no Iriun para evitar atrasos (lag) do Wi-Fi.
2. **Verifique o Índice da Câmara:**
   * No arquivo `mouse_gestual.py`, verifique a linha de inicialização:
     ```
     cap = cv2.VideoCapture(1)
     ```
   * Altere para `0`, `1` ou `2` dependendo de onde a sua câmara foi detetada. (Geralmente `1` para Iriun se já tiver uma webcam no portátil).
3. **Execute o Código:**
   ```
   python mouse_gestual.py
   ```
4. **Interface Visual:**
   * **Texto de Estado:** No canto superior esquerdo, o sistema diz o que está a detetar (ex: "MOVER", "CLIQUE", "ZOOM").
   * **Círculo Verde:** Indica que o modo "Mover Rato" está ativo na ponta do indicador.
   * **Retângulo Roxo:** É a sua "área de trabalho". Mova o dedo dentro desse retângulo para alcançar o ecrã todo sem esticar o braço.
   * **FPS:** Mostra a performance no canto inferior. Ideal acima de 25 FPS.
5. **Sair:**
   * Pressione a tecla `q` na janela da câmara para encerrar o programa.

## ⚙️ Configuração e Ajustes

Pode abrir o arquivo `mouse_gestual.py` e ajustar as variáveis no topo:

* **`smoothening = 4`** : Ajusta a suavização do movimento.
  * Valor maior = Rato mais suave, mas com leve atraso.
  * Valor menor = Resposta mais rápida, mas pode tremer um pouco.
* **`frame_reduction = 100`** : Tamanho da margem do ecrã.
  * Aumente este valor se tiver dificuldade em alcançar os cantos do ecrã ou se o retângulo roxo estiver muito grande.

## ⚠️ Solução de Problemas Comuns

**1. Erro: `AttributeError: module 'mediapipe' has no attribute 'solutions'`**

* Você está a usar versões incompatíveis. Execute o comando de instalação listado na secção "Pré-requisitos" deste README para forçar o downgrade do Protobuf e Numpy.

**2. A câmara abre mas o ecrã fica preto**

* Verifique se a aplicação Iriun no telemóvel está conectada (ecrã aceso).
* Tente alterar o índice do `cv2.VideoCapture(x)` para 0 ou 2 no código.

**3. O rato está a tremer muito**

* Melhore a iluminação do ambiente.
* Aumente o valor de `smoothening` no código.

**4. O sistema não deteta o indicador ("MOVER")**

* Certifique-se de que o dedo médio está bem dobrado. O sistema precisa de ver uma diferença clara entre a altura do indicador e a base do dedo médio.

**5. Baixo FPS (< 15)**

* Se estiver a usar Iriun via Wi-Fi, conecte via cabo USB.
* O código já possui redimensionamento de imagem para otimizar a performance.

## 📄 Licença

Este projeto é de código aberto e livre para uso educacional e pessoal.
