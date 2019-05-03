import imageio
import numpy as np
import scipy.ndimage as scnd

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
    return self._baseImage.copy()

  '''other: other image. x/y: x/y position of upper left of other. (can be negative)
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
            totpow = min(int(pixel[3]) + int(back[3]), 255)
            pixpow = pixel[3] /totpow
            backpow = (totpow - pixel[3]) / totpow
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

  ''' rolls the base by amount in the nesw direction.'''
  def roll(self, amount, nesw):
    if nesw.upper() == 'N':
      return np.roll(self._baseImage, -amount, axis = 0)
    if nesw.upper() == 'E':
      return np.roll(self._baseImage, amount, axis = 1)
    if nesw.upper() == 'S':
      return np.roll(self._baseImage, amount, axis = 0)
    if nesw.upper() == 'W':
      return np.roll(self._baseImage, -amount, axis = 1)
    return self.base()
  
  '''tilts image clockwise degrees. returns with transparent borders so that any angle would fit.'''
  def tilt(self, degrees):
    d = int(np.sqrt(self.size()[0]**2 + self.size()[1]**2) + 2)
    ret = np.full((d, d, 4), np.uint8(0))
    xmargin = (d - self.size()[1])//2
    ymargin = (d - self.size()[0])//2

    ret[ymargin:ymargin + self.size()[0], xmargin:xmargin + self.size()[1]] = self._baseImage

    return scnd.rotate(ret, degrees, axes=(0,1), reshape=False)

  '''sets alpha value to amount. amount can also be a mask.'''
  def setOpacity(self, amount):
    ret = self.base()
    ret[:,:,3] = amount
    return ret

  '''scales RGBA by vector'''
  def scaleRGBA(self, vector):
    ret = self.base()
    ret = ret * vector
    return np.uint8(ret)
  
  '''multiplies RGBA by matrix.'''
  def alterRGBA(self, matrix):
    ret = self.base()
    ret = np.matmul(ret, matrix)
    return np.uint8(ret)

  '''uses condintion function to make a 2D mask of the image where truth is 255 and flase is 0'''
  def maskFromCond(self, condition):
    def newAlpha(rgba):
      if condition(rgba):
        return 255
      else:
        return 0

    return np.array([[newAlpha(j) for j in i] for i in self._baseImage])



