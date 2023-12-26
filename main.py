import random
import time

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


detector = HandDetector(maxHands=1)
timer = 0
startbut = False
startGame = False

scores = [0, 0]

while True:
    bg_img = cv2.imread("Resources/BG.png")

    success, img = cap.read()

    imgScale = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScale = imgScale[:, 80:480]

    hands, img = detector.findHands(imgScale)

    if startGame:
        if startbut is False:
            timer = time.time() - initialTime
            cv2.putText(bg_img, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                startbut = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    rand_num = random.randint(1, 3)
                    AIimg = cv2.imread(f'Resources/{rand_num}.png', cv2.IMREAD_UNCHANGED)
                    bg_img = cvzone.overlayPNG(bg_img, AIimg, (149, 310))

                    if (playerMove == 1 and rand_num == 3) or (playerMove == 2 and rand_num == 1) or (playerMove == 3 and rand_num == 2):
                        scores[1] += 1

                    if (playerMove == 3 and rand_num == 1) or (playerMove == 1 and rand_num == 2) or (playerMove == 2 and rand_num == 3):
                        scores[0] += 1

    bg_img[234:654, 795:1195] = imgScale
    if startbut:
        bg_img = cvzone.overlayPNG(bg_img, AIimg, (149, 310))
    cv2.putText(bg_img, str((scores[0])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)
    cv2.putText(bg_img, str((scores[1])), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)

    cv2.imshow("BG", bg_img)
    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        startbut = False

