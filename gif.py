import numpy as np
import imageio
import image

class GifObj:
  '''fps: int frames per second, secs: float time of this list
  image: the filename of the image if gif is from an image.
  gif: the filename of the gif if ''' 
  def __init__(self, image=None, fps=None, secs=None, gif=None):
    self._frameCount = None
    self._durations = None
    self._frames = None
    
    if(image != None and secs != None and fps != None):
      self._frameCount = int(secs*fps)
      self._durations = [1/fps for i in range(self._frameCount)]
      self._frames = np.array([image.base() for i in range(self._frameCount)])
    elif (gif != None):
      print('gif input functionality not done yet.')

  def getFrames(self):
    return self._frames

  def getDurations(self):
    return self._durations

  def scalarToX(self, scale):
    return int(self._frames.shape[2] * scale)

  def scalarToY(self, scale):
    return int(self._frames.shape[1] * scale)

  def size(self):
    return self._frames.shape
  
  def roll(self, direction):
    horiz = 0
    if 'E' in direction.upper() or 'W' in direction.upper(): 
      horiz = 1
    posit = -1
    if 'S' in direction.upper() or 'E' in direction.upper(): 
      posit = 1
    
    for i in range(self._frameCount):
      theImage = image.Image(base=self._frames[i])
      portion = i/self._frameCount
      distance = theImage.scalarToX(portion)
      if horiz == 0:
        distance = theImage.scalarToY(portion)
      self._frames[i] = theImage.roll(distance, direction)

  def twirl(self, direction):
    way = 1
    if 'L' in direction.upper(): 
      way = -1
    frames = []
    for i in range(self._frameCount):
      theImage = image.Image(base=self._frames[i])
      angle = (360 + 360* way * i/self._frameCount) %360

      frames.append(theImage.tilt(angle))
    self._frames = np.array(frames)

  def colorShift(self):
    def contribution(center, x):
      if (center == 0 and x > 1/3):
        return max(0, 1 - 3*abs(x - 1))
      return  max(0, 1 - 3*abs(x - center))


    for i in range(self._frameCount):
      frac = i / self._frameCount

      uno = contribution(0, frac)
      dos = contribution(1/3, frac)
      tres = contribution(2/3, frac)



      matrix = np.array([[uno, dos, tres, 0], [tres, uno, dos, 0], [dos, tres, uno, 0], [0, 0, 0, 1]])
      

      theImage = image.Image(base=self._frames[i])
      self._frames[i] = theImage.alterRGBA(matrix)

  '''amount must be less than 0.5'''
  def shake(self, xAmount, yAmount, scalars=False):
    if (not scalars):
      xAmount = xAmount/self.size()[2]
      yAmount = yAmount/self.size()[1]

    frames = []
    for i in range(self._frameCount):
      theImage = image.Image(base=self._frames[i])
      x1 = theImage.scalarToX(np.random.rand() * xAmount)
      x2 = x1 + theImage.scalarToX(1-xAmount)

      y1 = theImage.scalarToY(np.random.rand() * yAmount)
      y2 = y1 + theImage.scalarToY(1-yAmount)
      frames.append(theImage.cropPad(x1, y1, x2, y2))
    self._frames = np.array(frames)

  #overlay one gif on another
  def overlay(self, other, x, y, alphas=True, scalars=False):
    if(scalars):
      x = self.scalarToX(x)
      y = self.scalarToY(y)

    frames = []
    for i in range(self._frameCount):
      theImage = image.Image(base=self._frames[i])
      otherImage = image.Image(base=other.getFrames()[i])

      frames.append(theImage.overlay(otherImage, x, y, alphas))
    self._frames = np.array(frames)

  #resize every image
  def reshape(self, x, y, scalars=False):
    if(scalars):
      x = self.scalarToX(x)
      y = self.scalarToY(y)

    frames = []
    for i in range(self._frameCount):
      theImage = image.Image(base=self._frames[i])
      frames.append(theImage.reshape(x, y))

    self._frames = np.array(frames)

  #change the number of frames and durations
  #def retime(self, frames, durations)