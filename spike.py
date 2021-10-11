# arquivo sera deletado futuramente. Este representa apenas os primeiros testes com webcam

import cv2

captura = cv2.VideoCapture(0)
flag = False

while(1):
  ret, frame = captura.read()
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  _, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)
  size = len(frame)
  if frame[50][size//2] == 0: color = (255, 255, 255)
  else: color = (0, 0, 0)
  frame = cv2.putText(frame, 'teste', (size//2,50), cv2.FONT_HERSHEY_COMPLEX, 1, color, )
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