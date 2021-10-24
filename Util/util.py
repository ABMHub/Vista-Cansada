import cv2
import numpy as np

color_white = (255, 255, 255)

def ratio (n1 : float, n2 : float) -> float:
  return min(n1, n2)/max(n1,n2)

def debug (name, img, debug = False):
  if debug is True: cv2.imshow(name, img)

def calcHomography(base, frame, base_des, base_keypoints):
  orb_frame = cv2.ORB_create()
  f_keypoints, f_des = orb_frame.detectAndCompute(frame, None)

  matcher = cv2.BFMatcher()
  matches = matcher.match(f_des, base_des)

  img_matches = cv2.drawMatches(frame, f_keypoints, base, base_keypoints, matches[:20],None)

  matches.sort(key=lambda x: x.distance, reverse=False)
  numGoodMatches = int(len(matches) * 0.15)
  matches = matches[:numGoodMatches]
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
  
  for i, match in enumerate(matches):
    points1[i, :] = f_keypoints[match.queryIdx].pt
    points2[i, :] = base_keypoints[match.trainIdx].pt

  return points1, points2, img_matches