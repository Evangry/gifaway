import imageio
import numpy as np
import image

cat = image.Image('pngs/Cat.png')
bloon = image.Image('pngs/Balloon.png')
world = image.Image('pngs/world.png')
world2 = image.Image('pngs/world2.png')
twoalt = image.Image(base=cat.cropPad(-10, 10, 50, 60))
imageio.imwrite('test.png', cat.tilt(45))
