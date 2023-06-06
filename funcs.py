from libs import *


def getFrames(file: str, target: str, start: int, end: int):
    if not os.path.exists(f"./{target}"):
        os.makedirs(target)
    vid = cv2.VideoCapture(file)
    i = 0
    ret, frame = vid.read()
    frames = np.zeros((end - start + 1, frame.shape[0], frame.shape[1], 3), dtype="uint8")
    while ret and i <= end:
        if i >= start and i <= end:
            cv2.imwrite(f"./{target}/frame_{i - start}.png", frame)
            frames[i - start] = frame
        i += 1
        ret, frame = vid.read()
    return frames.shape, frames


def maskPlayers(img: np.ndarray, c: str):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    Ylower = (140, 110, 71)
    Yupper = (217, 199, 155)

    Bupper = (100, 124, 182)
    Blower = (37, 60, 98)
    if c == "Y" or c == "y":
        maskY = cv2.inRange(imgRGB, Ylower, Yupper)
        return imgRGB, maskY
    maskB = cv2.inRange(imgRGB, Blower, Bupper)
    return imgRGB, maskB


def applyMask(img: np.ndarray, mask: np.ndarray):
    maskedImg = np.zeros(img.shape, dtype="uint8")
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i, j] == 255:
                maskedImg[i, j] = img[i, j]
            else:
                maskedImg[i, j] = np.array([255, 255, 255])
    return maskedImg


def joinImages(img1: np.ndarray, img2: np.ndarray):
    joinedImage = np.zeros(
        (img1.shape[0] if img1.shape[0] > img2.shape[0] else img2.shape[0], img1.shape[1] + img2.shape[1], 3),
        dtype="uint8")
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            joinedImage[i, j] = img1[i, j]
    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            joinedImage[i, j + img1.shape[1] - 1] = img2[i, j]
    return joinedImage
