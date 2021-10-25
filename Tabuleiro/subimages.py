import numpy as np
import cv2
from Util.util import color_white

class SubImages:
  def __init__(self, img):
    self.alt = np.size(img, 0)
    self.larg = np.size(img, 1)

    dimensoes = min(self.alt, self.larg)
    offset_alt = max(self.alt-self.larg, 0)//2
    offset_larg = max(self.larg-self.alt, 0)//2
    value1 = int(dimensoes*(1/3))
    value2 = int(dimensoes*(2/3))

    x0 = offset_larg
    x1 = value1 + offset_larg
    x2 = value2 + offset_larg
    x3 = self.larg - offset_larg

    y0 = offset_alt
    y1 = value1 + offset_alt
    y2 = value2 + offset_alt
    y3 = self.alt - offset_alt

    self.x = [x0, x1, x2, x3]
    self.y = [y0, y1, y2, y3]

    self.x_resized = [0, dimensoes//3, (dimensoes//3)*2, dimensoes]
    self.y_resized = [0, dimensoes//3, (dimensoes//3)*2, dimensoes]

    self.center = []
    self.center_resized = []
    
    for i in range(3):
      for j in range(3):
        self.center.append( ( int((self.x[j] + self.x[j+1])/2), int((self.y[i] + self.y[i+1])/2) ) )

    for i in range(3):
      for j in range(3):
        self.center_resized.append( ( int((self.x_resized[j] + self.x_resized[j+1])/2), int((self.y_resized[i] + self.y_resized[i+1])/2) ) )

  def linhasVelha(self, img):
    cor = (255, 255, 255)
    espessura = 3

    # verticais
    img = cv2.line(img, (self.x[1], self.y[0]), (self.x[1], self.y[3]), cor, espessura)
    img = cv2.line(img, (self.x[2], self.y[0]), (self.x[2], self.y[3]), cor, espessura)
    
    # horizontais
    img = cv2.line(img, (self.x[0], self.y[1]), (self.x[3], self.y[1]), cor, espessura)
    img = cv2.line(img, (self.x[0], self.y[2]), (self.x[3], self.y[2]), cor, espessura)

    return img

  def subimages(self, img):
    ret = []
    

    for i in range(3):
      for j in range(3):
        ret.append(img[self.y_resized[i]:self.y_resized[i+1], self.x_resized[j]:self.x_resized[j+1]])
        
    return ret

  def contorno(self):
    return [[self.x_resized[0], self.y_resized[0]], [self.x_resized[0], self.y_resized[3]], [self.x_resized[3], self.y_resized[3]], [self.x_resized[3], self.y_resized[0]]]

  def desenhaContorno(self, img, points):
    color = (255, 255, 255)
    img = cv2.line(img, np.array(points[0], np.int32), np.array(points[1], np.int32), color)
    img = cv2.line(img, np.array(points[1], np.int32), np.array(points[2], np.int32), color)
    img = cv2.line(img, np.array(points[2], np.int32), np.array(points[3], np.int32), color)
    img = cv2.line(img, np.array(points[3], np.int32), np.array(points[0], np.int32), color)

    return img

  def ganhador(self, img, jogo, homography):
    jogo = jogo[1]
    pt1 = self.center_resized[(jogo[0][0]*3)+jogo[0][1]]
    pt2 = self.center_resized[(jogo[1][0]*3)+jogo[1][1]]
    pts = [pt1, pt2]
    pts = cv2.perspectiveTransform(np.array([pts], dtype=np.float32), homography)[0]
    print(pts)
    return cv2.line(img, (int(pts[0][0]), int(pts[0][1])), (int(pts[1][0]), int(pts[1][1])), color_white, 5)

  def campo(self, img):
    return img[self.y[0]:self.y[3], self.x[0]:self.x[3]]