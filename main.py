import cv2
import numpy as np

captura = cv2.VideoCapture(0)
calibrado = False

while (calibrado is False):
  ret, frame_orig = captura.read()
  cv2.imshow('webcam', frame_orig)

  key = cv2.waitKey(30)
  if key == 32:
    base_image = frame_orig
    calibrado = True
  if key == 27:
    break

base_nomr = np.linalg.norm(base_image)
orb_base = cv2.ORB_create()
b_keypoints, b_des = orb_base.detectAndCompute(base_image, None)

while(1):
  ret, frame_orig = captura.read()
  frame = frame_orig

  orb_frame = cv2.ORB_create()
  f_keypoints, f_des = orb_frame.detectAndCompute(frame, None)

  matcher = cv2.BFMatcher()
  matches = matcher.match(f_des, b_des)

  final_img = cv2.drawMatches(frame, f_keypoints, base_image, b_keypoints, matches[:20],None)

  matches.sort(key=lambda x: x.distance, reverse=False)
  numGoodMatches = int(len(matches) * 0.15)
  matches = matches[:numGoodMatches]
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
  for i, match in enumerate(matches):
    points1[i, :] = f_keypoints[match.queryIdx].pt
    points2[i, :] = b_keypoints[match.trainIdx].pt
  try:
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
    # print('ugauga')
    height, width, _ = base_image.shape
    im1Reg = cv2.warpPerspective(frame, h, (width, height))
  except:
    print('deu ruim\n')
  print(np.linalg.norm(im1Reg), base_nomr) # tenta 95%
  cv2.imshow('teste2', im1Reg)
  cv2.imshow('teste', final_img)
  key = cv2.waitKey(30)
  if key == 27:
    break