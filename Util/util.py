import cv2
import numpy as np

color_white = (255, 255, 255)

def ratio (n1 : float, n2 : float) -> float:
  return min(n1, n2)/max(n1,n2)

def debug (name, img, debug = False):
  if debug is True: cv2.imshow(name, img)

def calcHomography(base, frame, base_des, base_keypoints):
  # keypoints e descriptors do frame atual
  orb_frame = cv2.ORB_create()
  frame_keypoints, frame_des = orb_frame.detectAndCompute(frame, None)

  # correspondencia entre os descriptors
  matcher = cv2.BFMatcher()
  matches = matcher.match(frame_des, base_des)

  # cria imagem com linhas fazendo o "match"
  img_matches = cv2.drawMatches(frame, frame_keypoints, base, base_keypoints, matches[:20],None)

  # filtra para so as 15% melhores matches
  matches.sort(key=lambda x: x.distance, reverse=False)
  numGoodMatches = int(len(matches) * 0.15)
  matches = matches[:numGoodMatches]

  # retorna keypoints relativos aos descriptors de cada correspondencia
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
  for i, match in enumerate(matches):
    points1[i, :] = frame_keypoints[match.queryIdx].pt
    points2[i, :] = base_keypoints[match.trainIdx].pt

  return points1, points2, img_matches