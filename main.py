import cv2
import numpy as np
from Tabuleiro.subimages import SubImages
from Util.util import calcHomography, ratio, color_white, debug
from Velha import jogoDaVelha

captura = cv2.VideoCapture(0)
calibrado = False
encerrar = False
debug_flag = False
xis = cv2.imread('x.png')

_, frame_teste = captura.read()
si = SubImages(frame_teste)
alt_frame = np.size(frame_teste, 0)
larg_frame = np.size(frame_teste, 1)
print("altura =", larg_frame, "largura =", alt_frame) # 640 480 nos testes

while (calibrado is False and encerrar is False):
  _, frame_orig = captura.read()
  frame_orig = si.linhasVelha(frame_orig)
  cv2.imshow('webcam', frame_orig)

  key = cv2.waitKey(30)
  if key == 32:
    calibrado = True
  if key == 27:
    encerrar = True

base_image = frame_orig
base_nomr = np.linalg.norm(base_image)

orb_base = cv2.ORB_create()
b_keypoints, b_des = orb_base.detectAndCompute(base_image, None)
img_rotacionada = frame_orig

mvCount = [0]*9
jogo = jogoDaVelha.JogoDaVelha()

while(encerrar is False):
  _, frame_orig = captura.read()

  points1, points2, img_matches = calcHomography(base_image, frame_orig, b_des, b_keypoints)

  try:
    homography, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
    height, width, _ = base_image.shape
    temp = cv2.warpPerspective(frame_orig, homography, (width, height))
    if ratio(np.linalg.norm(temp), base_nomr) > 0.8: img_rotacionada = temp

  except:
    print('Calculo inicial da homografia falhou')

  debug('teste2', img_rotacionada, debug_flag)
  debug('teste', img_matches, debug_flag)

  img_array = si.subimages(img_rotacionada)

  for i in range(len(img_array)):
    debug(f"elem {i}", img_array[i], debug_flag)
    maxval = cv2.minMaxLoc(cv2.matchTemplate(img_array[i], xis, cv2.TM_CCOEFF_NORMED))[1]

    if maxval > 0.4: 
      mvCount[i]+=1
      if mvCount[i] == 3:
        mvCount[i] = 0

        try:
          jogo.jogadaHumano((i//3, i%3))
        except Exception as err:
          print(err)
        else:
          jogo.jogadaMaquina()
          print(jogo.jogo)

    else:
      mvCount[i] = 0

  try:
    homography_inverse = np.linalg.inv(homography)
    detransformed = cv2.perspectiveTransform(np.array([si.contorno()], dtype=np.float32), homography_inverse)

    linhas = si.desenhaContorno(frame_orig, detransformed[0])
    cv2.imshow("revertida-reversa", linhas)

  except Exception as err:
    print(err)

  key = cv2.waitKey(30)
  if key == 27:
    encerrar = True