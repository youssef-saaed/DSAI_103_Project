from funcs import *

shape, frames = getFrames("vid.mp4", "./frames", 0, 95)

# img = cv2.cvtColor(frames[40],cv2.COLOR_BGR2RGB)
# img2 = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
# img2 = cv2.inRange(img2,108,255)
# img2 = cv2.blur(img2,(3,3))
# plt.imshow(img2,cmap="gray")
# plt.show()
