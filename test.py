import imageio
import numpy as np
import image

cat = image.Image('pngs/Cat.png')
ghostCat = image.Image(base = cat.scaleRGBA(np.array([1.0, 0.7, 1.0, 0.5])))

bloon = image.Image('pngs/Balloon.png')
world = image.Image('pngs/world.png')
world2 = image.Image('pngs/world2.png')


imageio.imwrite('test.png', world.overlay(ghostCat, 0, 0))

