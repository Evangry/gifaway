import imageio
import numpy as np

class Image:
  def __init__(self, filename):
    self._baseImage = imageio.imread(filename)
    if(self._baseImage.shape[2] == 3):
      alphas = np.array([[[np.uint8(255)] for i in range(self._baseImage.shape[0])] for j in range(self._baseImage.shape[1])])
      self._baseImage = np.append(self._baseImage, alphas, axis=2)

  def scalarToX(self, scale):
    return int(self._baseImage.shape[1] * scale)

  def scalarToY(self, scale):
    return int(self._baseImage.shape[0] * scale)

  '''other: other image. x: x position of upper left of other. y: same but y coord.'''
  def overlay(self, other, x, y):
    xend = min(x + other._baseImage.shape[1], self._baseImage.shape[1])
    yend = min(y + other._baseImage.shape[0], self._baseImage.shape[0])

    otherxend = xend - x
    otheryend = yend - y
    
    left = self._baseImage[:,:x]
    center = np.append(self._baseImage[:y,x:xend], other._baseImage[:otheryend,:otherxend], axis=0)
    center = np.append(center, self._baseImage[yend:, x:xend], axis=0)
    right = np.append(center, self._baseImage[:,xend:], axis=1)

    return np.append(left, right, axis=1)
  
  '''pos: x or y position of point of division. nesw: side of the point that's kept.'''
  def divide(self, pos, nesw):
    if(nesw.upper() == 'N'):
      return self._baseImage[:pos]
    if(nesw.upper() == 'E'):
      return self._baseImage[:,pos:]
    if(nesw.upper() == 'S'):
      return self._baseImage[pos:]
    if(nesw.upper() == 'W'):
      return self._baseImage[:,:pos]
    return self._baseImage

  






