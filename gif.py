import numpy as np
import imageio
import image

Class GifObj:
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
      self._frames = np.array([image for i in range(self._frameCount)])
    else if (gif != None):
      print('gif input functionality not done yet.')
  def getFrames(self):
    return self._frames

  def getDurations(self):
    return self._durations
  
