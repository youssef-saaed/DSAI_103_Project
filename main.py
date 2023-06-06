from funcs import *

shape, frames = getFrames("vid.mp4", "./frames", 737, 850)
detectedBallFrames = detectBall(frames, shape, (330, 184), 10)

for i in range(shape[0]):
    org, yellowPlayers = maskPlayers(frames[i], "Y")
    YAppliedMask = applyMask(org, yellowPlayers)
    joinedYP = joinImages(org, YAppliedMask)
    dispImg = cv2.cvtColor(joinedYP, cv2.COLOR_RGB2BGR)
    cv2.imshow("Yellow players mask", dispImg)
    if cv2.waitKey(1) == ord("q"):
        break
cv2.destroyAllWindows()

for i in range(shape[0]):
    org, bluePlayers = maskPlayers(frames[i], "B")
    BAppliedMask = applyMask(org, bluePlayers)
    joinedBP = joinImages(org, BAppliedMask)
    dispImg = cv2.cvtColor(joinedBP, cv2.COLOR_RGB2BGR)
    cv2.imshow("Blue players mask", dispImg)
    if cv2.waitKey(1) == ord("q"):
        break
cv2.destroyAllWindows()

for i in range(shape[0]):
    dispImg = cv2.cvtColor(detectedBallFrames[i], cv2.COLOR_RGB2BGR)
    cv2.imshow("Ball detection", dispImg)
    if cv2.waitKey(50) == ord("q"):
        break
cv2.destroyAllWindows()
