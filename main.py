import matplotlib.pyplot as plt

from funcs import *

shape, frames = getFrames("vid.mp4", "./frames", 0, 95)

img = cv2.cvtColor(frames[72], cv2.COLOR_BGR2RGB)

plt.imshow(img)
plt.show()
