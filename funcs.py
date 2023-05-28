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
