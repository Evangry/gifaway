import imageio
import numpy as np
import image
import gif

cat = image.Image('pngs/Cat.png')

bloon = image.Image('pngs/Danger.png')
world = image.Image('pngs/world.png')
world2 = image.Image('pngs/world2.png')

arr = np.array([[0, 0, 0, -0.5], [0, 1, 0, 1], [0, 0, 0, -0.5], [0, 0, 0, 0]])

bloonUp = gif.GifObj(image = image.Image(base=bloon.reshape(bloon.scalarToX(0.2), bloon.scalarToY(0.4))), fps=24, secs=2)
bloonUp.roll('N')
#bloonUp.twirl('L')
#bloonUp.colorShift()

worldWide = gif.GifObj(image=cat, fps=24, secs=2)
worldWide.shake(0, 0.06, scalars=True)
worldWide.overlay(bloonUp, 0.1, 0.1, scalars=True)

imageio.mimwrite('test.gif', worldWide.getFrames(), duration = worldWide.getDurations())

imageio.imwrite('test.png', bloon.reshape(bloon.scalarToX(2.0), bloon.scalarToY(2.0)))
