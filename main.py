import cv2
import numpy as np
from Tabuleiro.subimages import SubImages
from Util.util import ratio
from Velha import jogoDaVelha

captura = cv2.VideoCapture(0)
calibrado = False
encerrar = False
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

mvCount = [0]*9
jogo = jogoDaVelha.JogoDaVelha()

while(encerrar is False):
  ret, frame_orig = captura.read()
  frame = frame_orig

  orb_frame = cv2.ORB_create()
  f_keypoints, f_des = orb_frame.detectAndCompute(frame, None)

  matcher = cv2.BFMatcher()
  matches = matcher.match(f_des, b_des)

  img_matches = cv2.drawMatches(frame, f_keypoints, base_image, b_keypoints, matches[:20],None)

  matches.sort(key=lambda x: x.distance, reverse=False)
  numGoodMatches = int(len(matches) * 0.15)
  matches = matches[:numGoodMatches]
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
  
  for i, match in enumerate(matches):
    points1[i, :] = f_keypoints[match.queryIdx].pt
    points2[i, :] = b_keypoints[match.trainIdx].pt

  try:
    h, _ = cv2.findHomography(points1, points2, cv2.RANSAC)
    height, width, _ = base_image.shape
    temp = cv2.warpPerspective(frame, h, (width, height))
    if ratio(np.linalg.norm(temp), base_nomr) > 0.8: img_rotacionada = temp

  except:
    print('deu ruim\n')

  cv2.imshow('teste2', img_rotacionada)
  cv2.imshow('teste', img_matches)

  arr = si.subimages(img_rotacionada)

  for i in range(len(arr)):
    cv2.imshow(f"elem {i}", arr[i])
    maxval = cv2.minMaxLoc(cv2.matchTemplate(arr[i], xis, cv2.TM_CCOEFF_NORMED))[1]
    if maxval > 0.4: 
      # print(f'Match no {i}')
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

  key = cv2.waitKey(30)
  if key == 27:
    encerrar = True