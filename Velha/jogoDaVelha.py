# from cv2 import randn
import random
import numpy as np

class JogoDaVelha:
  def __init__(self):
    self.jogo = np.zeros((3, 3))
    self.movimentos = 0
    self.ganhador = (0, 0)
  
  def checaFim(self) -> tuple:
    p = 0
    for linha in range(3):
      for coluna in range(3):
        elem = self.jogo[linha][coluna]
        if elem == 0: break
        elif p == 0: p = elem
        elif p != elem: break
        if coluna == 2: 
          self.ganhador = (p, 0)
          return self.ganhador

    p = 0
    for coluna in range(3):
      for linha in range(3):
        elem = self.jogo[linha][coluna]
        if elem == 0: break
        elif p == 0: p = elem
        elif p != elem: break
        if linha == 2:
          self.ganhador = (p, 1)
          return self.ganhador

    p = 0
    for diagonal in range(3):
      elem = self.jogo[diagonal][diagonal]
      if elem == 0: break
      elif p == 0: p = elem
      elif p != elem: break
      if diagonal == 2:
        self.ganhador = (p, 2)
        return self.ganhador

    p = 0
    d1 = 0
    d2 = 2
    while(d1 < 3):
      elem = self.jogo[d1][d2]
      if elem == 0: break
      elif p == 0: p = elem
      elif p != elem: break
      if d1 == 2: 
        self.ganhador = (p, 3)
        return self.ganhador
      d1 += 1
      d2 -= 1

    if self.movimentos == 9:
      return (3, 0)

    return (0, 0)

  def jogadaHumano(self, coord : tuple) -> tuple:
    if (self.ganhador != (0, 0)):
      return self.ganhador

    if (self.jogo[coord[0]][coord[1]] != 0):
      raise ValueError("Jogada sobre outra, jogue em outro lugar")

    elif (0 > coord[0] > 2 or 0 > coord[1] > 2):
      raise ValueError("Jogada fora dos limites do tabuleiro")

    else:
      self.jogo[coord[0]][coord[1]] = 1
      self.movimentos += 1
      return self.checaFim()

  def jogadaMaquina(self, dificuldade = 0) -> tuple:
    if (self.ganhador != (0, 0)):
      return self.ganhador
      
    if (dificuldade == 0):
      possiveis = []
      for a in range(3):
        for b in range(3):
          if (self.jogo[a][b] == 0):
            possiveis.append((a, b))

      jogada = possiveis[random.randint(0, len(possiveis)-1)]
      self.jogo[jogada[0]][jogada[1]] = 2
      self.movimentos += 1
      return self.checaFim()