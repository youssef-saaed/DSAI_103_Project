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


def getNewBallPosition(cballMask: np.ndarray, lPosition: tuple, threshold: float, ballSize, change: int):
    upM = lPosition[1] - change
    downM = lPosition[1] + change
    rightM = lPosition[0] + change
    leftM = lPosition[0] - change
    up = sum(sum(cballMask[upM:upM + ballSize, lPosition[0]:lPosition[0] + ballSize]))
    down = sum(sum(cballMask[downM:downM + ballSize, lPosition[0]:lPosition[0] + ballSize]))
    right = sum(sum(cballMask[lPosition[1]:lPosition[1] + ballSize, rightM:rightM + ballSize]))
    left = sum(sum(cballMask[lPosition[1]:lPosition[1] + ballSize, leftM:leftM + ballSize]))
    upRight = sum(sum(cballMask[upM:upM + ballSize, rightM:rightM + ballSize]))
    upLeft = sum(sum(cballMask[upM:upM + ballSize, leftM:leftM + ballSize]))
    downRight = sum(sum(cballMask[downM:downM + ballSize, rightM:rightM + ballSize]))
    downLeft = sum(sum(cballMask[downM:downM + ballSize, leftM:leftM + ballSize]))
    center = sum(sum(cballMask[lPosition[1]:lPosition[1] + ballSize, lPosition[0]:lPosition[0] + ballSize]))
    if not (center >= 2500 - 2500 * threshold):
        maxDens = max(up, down, right, left, upRight, downRight, upLeft, downLeft)
        if maxDens == up:
            lPosition = (lPosition[0], lPosition[1] - change)
        elif maxDens == down:
            lPosition = (lPosition[0], lPosition[1] + change)
        elif maxDens == right:
            lPosition = (lPosition[0] + change, lPosition[1])
        elif maxDens == left:
            lPosition = (lPosition[0] - change, lPosition[1])
        elif maxDens == upRight:
            lPosition = (lPosition[0] + change, lPosition[1] - change)
        elif maxDens == downRight:
            lPosition = (lPosition[0] + change, lPosition[1] + change)
        elif maxDens == upLeft:
            lPosition = (lPosition[0] - change, lPosition[1] - change)
        elif maxDens == downLeft:
            lPosition = (lPosition[0] - change, lPosition[1] + change)
    return lPosition


def detectBall(frames: np.ndarray, size: tuple, initialPos: tuple, ballSize):
    markedFrames = frames.copy()
    mFrame = cv2.cvtColor(markedFrames[0], cv2.COLOR_BGR2RGB)
    ballLower = (180, 180, 180)
    ballUpper = (255, 255, 255)
    ballMask = cv2.inRange(mFrame, ballLower, ballUpper)
    lPosition = initialPos
    cv2.rectangle(mFrame, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
    cv2.rectangle(ballMask, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
    markedFrames[0] = mFrame
    threshold = 0.7
    movementDiv = 2
    change = ballSize // movementDiv
    for i in range(1, size[0]):
        cFrame = cv2.cvtColor(markedFrames[i], cv2.COLOR_BGR2RGB)
        cballMask = cv2.inRange(cFrame, ballLower, ballUpper)
        lPosition = getNewBallPosition(cballMask, lPosition, threshold, ballSize, change)
        cv2.rectangle(cFrame, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
        cv2.rectangle(cballMask, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
        markedFrames[i] = cFrame
    return markedFrames
