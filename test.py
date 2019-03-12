import imageio
import numpy as np
import image

cat = image.Image('Cat.png')
bloon = image.Image('Balloon.png')
world = image.Image('world.png')
imageio.imwrite('test.png', world.overlay(bloon, 150, 150))
