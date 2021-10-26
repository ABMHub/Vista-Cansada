import cv2
import numpy as np
from Tabuleiro.subimages import SubImages
from Util.util import calcHomography, ratio, color_white, debug
from Velha import jogoDaVelha

# inicializacao de flags e inputs
captura = cv2.VideoCapture(0)
calibrado = False
encerrar = False
debug_flag = False
xis = cv2.imread('XIS_800_800.png') # template de X 800x800 (sera redimensionado abaixo)

# inicializa classe de subimagens com uma imagem da camera
_, frame_teste = captura.read()
si = SubImages(frame_teste)

# descobre tamanho otimo para o template do X
alt_frame = np.size(frame_teste, 0)
larg_frame = np.size(frame_teste, 1)
div = int(min(alt_frame, larg_frame)/6.4)
xis = cv2.resize(xis, (div, div))

# secao de calibracao
while (calibrado is False and encerrar is False):
  _, frame_orig = captura.read()
  linhas = frame_orig.copy()
  # desenha linhas de referencia
  linhas = si.linhasVelha(linhas)
  cv2.imshow('calibragem', linhas)

  key = cv2.waitKey(30)
  if key == 32:       # barra de espaco
    calibrado = True
  if key == 27:       # esc
    encerrar = True

# recorta tabuleiro e salva imagem base da calibracao
base_image = si.campo(frame_orig)

# pre calculado - usado para computar diferenca entre o frame calibrado e o atual
base_nomr = np.linalg.norm(base_image)

# pre calculado - descriptors e keypoints
orb_base = cv2.ORB_create()
b_keypoints, b_des = orb_base.detectAndCompute(base_image, None)

# inicializa variável
img_rotacionada = frame_orig

# inicializa jogo da velha
mvCount = [0]*9
jogo = jogoDaVelha.JogoDaVelha()

# reseta janelas
cv2.destroyAllWindows()

# loop do jogo
while(encerrar is False):
  _, frame_orig = captura.read()

  # calcula homografia entre a imagem atual e a calibrada
  points1, points2, img_matches = calcHomography(base_image, frame_orig, b_des, b_keypoints)

  # gera mudancao de perspectiva pela homografia
  try:
    homography, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
    height, width, _ = base_image.shape
    temp = cv2.warpPerspective(frame_orig, homography, (width, height))
    # se for muito diferente da calibracao, nao faz nada e reseta contadores
    if ratio(np.linalg.norm(temp), base_nomr) > 0.8: img_rotacionada = temp
    else: mvCount = [0 for i in range(9)]

  except:
    if debug_flag is True: print('Calculo inicial da homografia falhou')

  debug('teste2', img_rotacionada, debug_flag)
  debug('teste', img_matches, debug_flag)

  img_array = si.subimages(img_rotacionada)

  for i in range(len(img_array)):
    debug(f"elem {i}", img_array[i], debug_flag)
    maxval = cv2.minMaxLoc(cv2.matchTemplate(img_array[i], xis, cv2.TM_CCOEFF_NORMED))[1]

    # se houve match com template
    if maxval > 0.4: 
      mvCount[i]+=1
      # se o X foi detectado por 3 frames consecutivos, entao computa
      if mvCount[i] == 3:
        mvCount[i] = 0

        try:
          jogo.jogadaHumano((i//3, i%3)) # jogada do humano
        except Exception as err:
          if debug_flag is True: print(err)
        else:
          jogo.jogadaMaquina()
          print(jogo.jogo)

    else:
      mvCount[i] = 0

  # cria array com todos os circulos computados
  bolinhas = []
  for i in range(3):
    for j in range(3):
      if jogo.jogo[i][j] == 2:
        centro = si.center_resized[(i*3)+j]
        bolinhas.append(centro)
        bolinhas.append((centro[0], centro[1]+(si.lado_campo*0.3))) # ponto para determinar o raio do circulo

  # encontra homografia inversa
  try:
    homography_inverse = np.linalg.inv(homography)
    borda = cv2.perspectiveTransform(np.array([si.contorno()], dtype=np.float32), homography_inverse)
    img_final = si.desenhaContorno(frame_orig, borda[0])

    # desenha circunferencias
    if len(bolinhas) != 0:
      circulos = cv2.perspectiveTransform(np.array([bolinhas], dtype=np.float32), homography_inverse)[0]
      for i in range(0, len(circulos), 2):
        circulo = circulos[i]
        img_final = cv2.circle(img_final, (int(circulo[0]), int(circulo[1])), int(np.linalg.norm(circulos[i] - circulos[i+1])), color_white, 3)

    cv2.imshow("jogo", img_final)

  except Exception as err:
    if debug_flag is True: print(err)

  if (jogo.ganhador != (0, 0)): encerrar = True

  key = cv2.waitKey(30)
  if key == 27:
    encerrar = True

print(jogo.ganhador)
# se ninguem ganhou pula essa etapa
if jogo.ganhador[0] != 0 and jogo.ganhador[0] != 3:
  img_final = si.ganhador(img_final, jogo.ganhador, homography_inverse)
  cv2.imshow("jogo", img_final)

if jogo.ganhador[0] == 3:
  cv2.imshow("jogo", img_final)

cv2.waitKey()
cv2.destroyAllWindows()