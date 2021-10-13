# from cv2 import randn
import random
import numpy as np

class JogoDaVelha:
  def __init__(self):
    self.jogo = np.zeros((3, 3))
    self.movimentos = 0
  
  def checaFim(self) -> tuple:
    p = 0
    for linha in range(3):
      for coluna in range(3):
        elem = self.jogo[linha][coluna]
        if elem == 0: break
        elif p == 0: p = elem
        elif p != elem: break
        if coluna == 2: return (p, 0)

    p = 0
    for coluna in range(3):
      for linha in range(3):
        elem = self.jogo[linha][coluna]
        if elem == 0: break
        elif p == 0: p = elem
        elif p != elem: break
        if linha == 2: return (p, 1)

    p = 0
    for diagonal in range(3):
      elem = self.jogo[diagonal][diagonal]
      if elem == 0: break
      elif p == 0: p = elem
      elif p != elem: break
      if diagonal == 2: return (p, 2)

    p = 0
    d1 = 0
    d2 = 2
    while(d1 < 3):
      elem = self.jogo[d1][d2]
      if elem == 0: break
      elif p == 0: p = elem
      elif p != elem: break
      if d1 == 2: return (p, 3)
      d1 += 1
      d2 -= 1

    if self.movimentos == 9:
      return (3, 0)

    return (0, 0)

  def jogadaHumano(self, coord : tuple) -> tuple:
    if (self.jogo[coord[0]][coord[1]] != 0):
      raise "Jogada sobre outra, jogue em outro lugar"

    elif (0 > coord[0] > 2 or 0 > coord[1] > 2):
      raise "Jogada fora dos limites do tabuleiro"

    else:
      self.jogo[coord[0]][coord[1]] = 1
      self.movimentos += 1
      return self.checaFim()

  def jogadaMaquina(self, dificuldade : int) -> tuple:
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

jogo = JogoDaVelha()
while(1):
  print(jogo.jogo)
  if jogo.jogadaMaquina(0)[0] != 0: break
  print(jogo.jogo)
  inp = [int(x) for x in input().split()]
  if jogo.jogadaHumano(inp)[0] != 0: break

print(jogo.jogo)
print(jogo.checaFim())