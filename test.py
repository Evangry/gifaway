import imageio
import numpy as np
import image
import gif

cat = image.Image('pngs/Cat.png')

bloon = image.Image('pngs/Danger.png')
world = image.Image('pngs/world.png')
world2 = image.Image('pngs/world2.png')

arr = np.array([[0, 0, 0, -0.5], [0, 1, 0, 1], [0, 0, 0, -0.5], [0, 0, 0, 0]])

bloonUp = GifObj(image=bloon, fps=30, secs=1)

imageio.mimsave('test.gif', bloonup.getFrames(), duration = bloonUp.getDurations())

