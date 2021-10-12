# arquivo sera deletado futuramente. Este representa apenas os primeiros testes com webcam

import cv2
import imutils
import numpy as np

captura = cv2.VideoCapture(0)
flag = False

while(1):
  ret, frame_orig = captura.read()
  frame = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2GRAY)
  frame = cv2.GaussianBlur(frame, (7, 7), 3)
  frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  frame = cv2.bitwise_not(frame)
  frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, np.ones((3, 3)))
  # _, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)
  # cv2.imshow("tophat", frame)
  cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
  size = len(frame)

  puzzleCnt = cnts[0]

  for c in cnts:
    # approximate the contour
    # c = cnts[0]
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if our approximated contour has four points, then we can
    # assume we have found the outline of the puzzle
    if len(approx) == 4 or len(approx) == 20:
      puzzleCnt = approx
      print(len(puzzleCnt))
      break

  # puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
  # warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))

  output = frame_orig.copy()
  cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)
  cv2.imshow("Puzzle Outline", output)
  # cv2.waitKey(0)

  if frame[50][size//2] == 0: color = (255, 255, 255)
  else: color = (0, 0, 0)
  frame = cv2.putText(frame, 'teste', (size//2,50), cv2.FONT_HERSHEY_COMPLEX, 1, color, )
  cv2.imshow("Video orig", frame_orig)
  cv2.imshow("Video", frame)

  if flag is True:
    print('a') 
  
  k1 = cv2.waitKey(100)
  # k2 = k1 & 0xff              # mascaramento de bits possivelmente necessario para linux
  # print(k1, k2)
  if k1 == 32:
    image = frame
    flag = True
  if k1 == 27:
    break

captura.release()
cv2.destroyAllWindows()