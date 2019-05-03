import imageio
import numpy as np
import image
import gif

cat = image.Image('pngs/Cat.png')

bloon = image.Image('pngs/Danger.png')
world = image.Image('pngs/world.png')
world2 = image.Image('pngs/world2.png')

arr = np.array([[0, 0, 0, -0.5], [0, 1, 0, 1], [0, 0, 0, -0.5], [0, 0, 0, 0]])

bloonUp = gif.GifObj(image=bloon, fps=30, secs=3)
#bloonUp.roll('N')
#bloonUp.twirl('L')
#bloonUp.colorShift()

worldWide = gif.GifObj(image=cat, fps=24, secs=2)
worldWide.shake(0, 0.06)

imageio.mimwrite('test.gif', worldWide.getFrames(), duration = worldWide.getDurations())

#imageio.imwrite('test.png', bloonUp.getFrames()[17])
