# Import funcs module which have all our functions which are manipulated in this file
from funcs import *

# Get and save all our selected frames and put them in numpy array and get its shape and the array itself
shape, frames = getFrames("vid.mp4", "./frames", 737, 850)
shape_2, frames_2 = getFrames("vid.mp4", "./frames_2", 1544, 1833)

# Get all frames with rectangle mark on the ball in each frame and positions coordinates
detectedBallFrames, detectedBallPositions = detectBall(frames, shape, (330, 184), 10)

# Loop over every frame and use maskPlayer function on the frame with "Y" argument to mask players in yellow t-shirts
# Then apply mask on original image then convert color to BGR to display using cv2
# Lastly there is a condition to wait "q" key from user for 1ms and if pressed break the loop otherwise it continue to next frame
for i in range(shape[0]):
    # maskPlayers function get the current loop frame and take "Y" argument, so it return original frame in RGB and yellowPlayers mask
    org, yellowPlayers = maskPlayers(frames[i], "Y")

    # Applying yellow players mask on the original frame to get an img that includes pixels of players with white background
    YAppliedMask = applyMask(org, yellowPlayers, "White")

    # Joining original frame and applied mask photo to be beside each other in one photo
    joinedYP = joinImages(org, YAppliedMask)

    # Convert the joined image to BGR mode to display correct colors for cv2
    dispImg = cv2.cvtColor(joinedYP, cv2.COLOR_RGB2BGR)

    # Displaying image
    cv2.imshow("Yellow players mask", dispImg)

    # If condition which wait from user to press "q" key to break the loop before going to the next frame
    if cv2.waitKey(1) == ord("q"):
        break

# Destroy the cv2 window after the loop ends
cv2.destroyAllWindows()

# Loop over every frame and use maskPlayer function on the frame with "B" argument to mask players in Blue t-shirts
# Then apply mask on original image then convert color to BGR to display using cv2
# Lastly make condition to wait "q" key from user for 1ms and if pressed break the loop otherwise it continue to next frame
for i in range(shape[0]):
    # maskPlayers function get the current loop frame and take "B" argument, so it return original frame in RGB and bluePlayers mask
    org, bluePlayers = maskPlayers(frames[i], "B")

    # Applying blue players mask on the original frame to get an img that includes pixels of players with white background
    BAppliedMask = applyMask(org, bluePlayers, "White")

    # Joining original frame and applied mask photo to be beside each other in one photo
    joinedBP = joinImages(org, BAppliedMask)

    # Convert the joined image to BGR mode to display correct colors for cv2
    dispImg = cv2.cvtColor(joinedBP, cv2.COLOR_RGB2BGR)

    # Displaying image
    cv2.imshow("Blue players mask", dispImg)

    # If condition which wait from user to press "q" key to break the loop before going to the next frame
    if cv2.waitKey(1) == ord("q"):
        break

# Destroy the cv2 window after the loop ends
cv2.destroyAllWindows()

# Loop over detectedBallFrames array and convert every frame colors to BGR
# Then there is a condition to wait "q" key from user for 1ms and if pressed break the loop otherwise it continue to next frame
for i in range(shape[0]):
    # Convert the joined image to BGR mode to display correct colors for cv2
    dispImg = cv2.cvtColor(detectedBallFrames[i], cv2.COLOR_RGB2BGR)

    # Adding coordinates text to image
    cv2.putText(dispImg, f"Pos: ( {detectedBallPositions[i][0]} , {detectedBallPositions[i][0]} )", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Displaying image
    cv2.imshow("Ball detection", dispImg)

    # If condition which wait from user to press "q" key to break the loop before going to the next frame
    if cv2.waitKey(75) == ord("q"):
        break

# Destroy the cv2 window after the loop ends
cv2.destroyAllWindows()

xCS, xCE = getFirstFrameCenter(frames_2[0])

for i in range(shape_2[0]):
    xCS, xCE, mask, region = getRegion(frames_2[i], xCS, xCE)
    appliedMaskImg = applyMask(frames_2[i], mask, "Black")
    joinedRegionFrames = joinImages(frames_2[i], appliedMaskImg)
    cv2.putText(joinedRegionFrames, f"Region: {region}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.imshow("Region labeling", joinedRegionFrames)
    if cv2.waitKey(1) == ord("q"):
        break
cv2.destroyAllWindows()
