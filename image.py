import imageio
import numpy as np

class Image:
  def __init__(self, filename=None, base=None):
    self._baseImage = None
    if filename != None:
      self._baseImage = imageio.imread(filename)
      self.addAlphas()
    elif base.any() != None:
      self._baseImage = base
      self.addAlphas()
 

  '''adds alpha values if they aren't there.'''
  def addAlphas(self):
    if(self._baseImage.shape[2] == 3):
      alphas = np.array([[[np.uint8(255)] for i in range(self._baseImage.shape[0])] for j in range(self._baseImage.shape[1])])
      self._baseImage = np.append(self._baseImage, alphas, axis=2)

  def scalarToX(self, scale):
    return int(self._baseImage.shape[1] * scale)

  def scalarToY(self, scale):
    return int(self._baseImage.shape[0] * scale)

  def size(self):
    return self._baseImage.shape

  def base(self):
    return self._baseImage[:]

  '''other: other image. x: x position of upper left of other. y: same but y coord.
     alphas: whether it's going to act according to alpha values in self and other.'''
  def overlay(self, other, x, y, alphas=True):
    xend = min(x + other._baseImage.shape[1], self._baseImage.shape[1])
    yend = min(y + other._baseImage.shape[0], self._baseImage.shape[0])

    otherx = max(0, -x)
    othery = max(0, -y)

    otherxend = xend - x
    otheryend = yend - y

    x = max(0, x)
    y = max(0, y)
    
    left = self._baseImage[:,:x]
    over = other._baseImage[othery:otheryend, otherx:otherxend]
    if alphas:
      for j in range(len(over)):
        for i in range(len(over[j])):
          pixel = over[j, i]
          if (pixel[3] < 255):
            back = self._baseImage[y+j, x+i]
            totpow = min(pixel[3] + back[3], 255)
            pixpow = pixel[3] /totpow
            backpow = (totpow - pixpow) / totpow
            pixel = np.array([np.uint8(pixel[k] * pixpow + back[k] * backpow) for k in range(4)])
            pixel[3] = np.uint8(totpow)
            over[j, i] = pixel
  

        

    center = np.append(self._baseImage[:y,x:xend], over, axis=0)
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
    return self.base()
  
  '''other: other picture. nesw: direction other picture is of self.'''
  def append(self, other, nesw):
    if(nesw.upper() == 'N' and self.size()[1] == other.size()[1]):
      return np.append(other._baseImage, self._baseImage, axis=0)
    if(nesw.upper() == 'E' and self.size()[0] == other.size()[0]):
      return np.append(self._baseImage, other._baseImage, axis=1)
    if(nesw.upper() == 'S' and self.size()[1] == other.size()[1]):
      return np.append(self._baseImage, other._baseImage, axis=0)
    if(nesw.upper() == 'W' and self.size()[0] == other.size()[0]):
      return np.append(other._baseImage, self._baseImage, axis=1)
    return self.base()

  '''this streches the image. x: x size of the returned image. y: same but for y'''
  def reshape(self, x, y):
    x1 = self.size()[1]
    y1 = self.size()[0]
    return np.array([[self._baseImage[int(j*y1/y),int(i*x1/x)] for i in range(x)] for j in range(y)])
  
  '''this resizes the image, adding alpha = 0 where the image isn't.
     x1/y1: coords of upper left corner (may be negative). x2/y2 coords of bottom right.'''
  def cropPad(self, x1, y1, x2, y2):
    blank = Image(base = np.full((y2-y1, x2-x1, 4), np.uint8(0)))
  
    return blank.overlay(self, -x1, -y1, alphas = False)






