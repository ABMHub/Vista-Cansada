import numpy as np
import cv2

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
        ret.append(img[self.y[i]:self.y[i+1], self.x[j]:self.x[j+1]])
        
    return ret