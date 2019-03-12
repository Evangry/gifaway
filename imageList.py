import numpy as np
import imageio

Class ImageList:
  '''filename: string name of image, typically ends with .png or .jpg
  fps: int frames per second, secs: float time of this list''' 
  def __init__(self, filename, fps, secs):
    self._frameCount = int(secs*fps)
    self._durations = [1/fps for i in range(self._frameCount)]
    self._baseImage = imageio.imread(filename)
    self._frames = np.array([self.baseImage for i in range(self._frameCount)])
    
  def getFrames(self):
    return self._frames
  
