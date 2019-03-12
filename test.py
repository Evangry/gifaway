import imageio
import numpy as np
import image

cat = image.Image('pngs/Cat.png')
bloon = image.Image('pngs/Balloon.png')
world = image.Image('pngs/world.png')
world2 = image.Image('pngs/world2.png')
twoalt = image.Image(base=world2.divide(world2.scalarToX(0.5), 'e'))
imageio.imwrite('test.png', world.reshape(200, 200))
