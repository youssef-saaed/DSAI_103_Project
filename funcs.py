# Import libs module which have all needed libraries
from libs import *


# Defining getFrames function which takes video file path and target location for saving frames and starting frame and ending frame
# It save frames selected in targeted location and return numpy array with frames in the second return and in the first return the shape of that array
def getFrames(file: str, target: str, start: int, end: int):
    # Checking if the targeted place for saving doesn't exist it is created
    if not os.path.exists(f"./{target}"):
        os.makedirs(target)

    # Creating VideoCapture object with the file location
    vid = cv2.VideoCapture(file)

    # Defining i for iterating
    i = 0

    # Read the first frame in the video with read() function which return boolean of success and the upcoming frame
    ret, frame = vid.read()

    # Creating a numpy array which will be a container for the frames
    frames = np.zeros((end - start + 1, frame.shape[0], frame.shape[1], 3), dtype="uint8")

    # Looping until the video end or the ending frame number come
    # In every iteration, if i in the range of selected frames numbers it save this frame in the targeted location
    # Then increase i by 1 and read the upcoming frame
    while ret and i <= end:
        if i >= start and i <= end:
            cv2.imwrite(f"./{target}/frame_{i - start}.png", frame)
            frames[i - start] = frame
        i += 1
        ret, frame = vid.read()

    # At the end returning numpy array "frames" shape and array itself
    return frames.shape, frames


# Defining maskPlayers function which take the frame and player color
# It return the original frame in RGB and the mask of players
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


# Defining applyMask function which take frame and a mask for that frame
# It return a new image that have frame pixels which only exists in the mask
def applyMask(img: np.ndarray, mask: np.ndarray, bg: str):
    maskedImg = np.zeros(img.shape, dtype="uint8")
    bgcolor = [0, 0, 0] if bg == "Black" or bg == "black" else [255, 255, 255]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if mask[i, j] == 255:
                maskedImg[i, j] = img[i, j]
            else:
                maskedImg[i, j] = np.array(bgcolor)

    return maskedImg


# This function defined takes two images and join them in new image with a width of sum of two images width and height with the highest height of two images
# It join the two picture by putting the first image in the new created image and then put the second image in the end position of first image and then return joined image
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


# This function take ball mask, last position for ball, threshold for change, ball size and position change amount for testing
# It returns new position
def getNewBallPosition(cballMask: np.ndarray, lPosition: tuple, threshold: float, ballSize: int, change: int):
    # Defining position change for its direction
    upM = lPosition[1] - change
    downM = lPosition[1] + change
    rightM = lPosition[0] + change
    leftM = lPosition[0] - change

    # Calculating pixel density in each direction
    up = sum(sum(cballMask[upM:upM + ballSize, lPosition[0]:lPosition[0] + ballSize]))
    down = sum(sum(cballMask[downM:downM + ballSize, lPosition[0]:lPosition[0] + ballSize]))
    right = sum(sum(cballMask[lPosition[1]:lPosition[1] + ballSize, rightM:rightM + ballSize]))
    left = sum(sum(cballMask[lPosition[1]:lPosition[1] + ballSize, leftM:leftM + ballSize]))
    upRight = sum(sum(cballMask[upM:upM + ballSize, rightM:rightM + ballSize]))
    upLeft = sum(sum(cballMask[upM:upM + ballSize, leftM:leftM + ballSize]))
    downRight = sum(sum(cballMask[downM:downM + ballSize, rightM:rightM + ballSize]))
    downLeft = sum(sum(cballMask[downM:downM + ballSize, leftM:leftM + ballSize]))
    center = sum(sum(cballMask[lPosition[1]:lPosition[1] + ballSize, lPosition[0]:lPosition[0] + ballSize]))

    # If the current position pixel density is less than threshold density the new position is the maximum pixel density's position
    if center <= 2500 - 2500 * threshold:
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

    # Returning new position
    return lPosition


# Defining detectBall function which take the frames for detection, shape of frames numpy array, initial position and ballSize
# It returns copy of frames array which have rectangle marks follow ball position and positions array
def detectBall(frames: np.ndarray, size: tuple, initialPos: tuple, ballSize: int):
    markedFrames = frames.copy()
    positions = np.zeros((size[0], 2))
    mFrame = cv2.cvtColor(markedFrames[0], cv2.COLOR_BGR2RGB)
    ballLower = (180, 180, 180)
    ballUpper = (255, 255, 255)
    ballMask = cv2.inRange(mFrame, ballLower, ballUpper)
    lPosition = initialPos
    positions[0] = np.array(lPosition)
    cv2.rectangle(mFrame, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
    cv2.rectangle(ballMask, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
    markedFrames[0] = mFrame
    threshold = 0.7
    movementDiv = 5
    change = ballSize // movementDiv
    for i in range(1, size[0]):
        cFrame = cv2.cvtColor(markedFrames[i], cv2.COLOR_BGR2RGB)
        cballMask = cv2.inRange(cFrame, ballLower, ballUpper)
        lPosition = getNewBallPosition(cballMask, lPosition, threshold, ballSize, change)
        positions[i] = np.array(lPosition)
        cv2.rectangle(cFrame, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
        cv2.rectangle(cballMask, lPosition, (lPosition[0] + ballSize, lPosition[1] + ballSize), (255, 0, 0), 1)
        markedFrames[i] = cFrame
    return markedFrames, positions


def dist(point1: tuple, point2: tuple):
    return ((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2) ** 0.5


def getFirstFrameCenter(frame: np.ndarray):
    lower = (75, 119, 95)
    upper = (114, 152, 133)
    mask = cv2.inRange(frame, lower, upper)
    points = []
    for i in range(len(mask)):
        rowPoints = []
        c = 0
        for j in range(len(mask[0])):
            if mask[i, j] == 255:
                c += 1
            else:
                c = 0
            if c >= 3:
                rowPoints.append((j - 1, i))
                c = 0
            points.append(rowPoints)
    threshold = 0.1
    maxDistRow = -1
    maxDist = 0
    for i in range(len(points)):
        if len(points[i]) >= 3:
            dist1 = dist(points[i][0], points[i][1])
            dist2 = dist(points[i][1], points[i][2])
            if dist1 >= (dist2 - dist2 * threshold) and dist1 <= (dist2 + dist2 * threshold):
                if (dist1 + dist2) > maxDist:
                    maxDist = dist1 + dist2
                    maxDistRow = i
    xStartPos = points[maxDistRow][0][0] - 5
    xEndPos = points[maxDistRow][2][0] + 5
    return xStartPos, xEndPos


def getRegion(frame: np.ndarray, xStartPos: int, xEndPos: int):
    lower = (75, 119, 95)
    upper = (114, 152, 133)
    move = 20
    threshold = 0.1
    mask = cv2.inRange(frame, lower, upper)
    current = sum(sum(mask[:, xStartPos:xEndPos]))
    right = sum(sum(mask[:, xStartPos + move:xEndPos + move]))
    left = sum(sum(mask[:, xStartPos - move:xEndPos - move]))
    maxDens = max(current, right, left)
    if maxDens != current or abs(maxDens - current) > (maxDens * threshold):
        if maxDens == right:
            xStartPos += move
            xEndPos += move
        else:
            xStartPos -= move
            xEndPos -= move
    if xStartPos < 150:
        return xStartPos, xEndPos, mask, "Right"
    elif xStartPos > 230:
        return xStartPos, xEndPos, mask, "Left"
    else:
        return xStartPos, xEndPos, mask, "Center"
