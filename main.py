import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    # Buttons
    button_list_values = [['7', '8', '9', '*'],
                          ['4', '5', '6', '-'],
                          ['1', '2', '3', '+'],
                          ['0', '/', '.', '=']]

    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 2)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70),
                    cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def check_click(self, x, y, img):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False


def main():
    button_list = []
    for x in range(4):
        for y in range(4):
            x_pos: int = x * 100 + 800
            y_pos = y * 100 + 150
            button_list.append(Button((x_pos, y_pos), 100, 100, Button.button_list_values[y][x]))

    # Variables
    my_equation = ''
    delay_counter = 0
    # Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while True:
        # Get image frame
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)

        # Draw All
        cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100),
                      (225, 225, 225), cv2.FILLED)

        cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100),
                      (50, 50, 50), 3)
        for button in button_list:
            button.draw(img)

        # Check for Hand
        if hands:
            # Find distance between fingers
            lm_list = hands[0]['lmList']
            length, _, img = detector.findDistance(lm_list[8], lm_list[12], img)
            print(length)
            x, y = lm_list[8]

            # If clicked check which button and perform action
            if length < 45 and delay_counter == 0:
                for i, button in enumerate(button_list):
                    if button.check_click(x, y, img):
                        my_value = Button.button_list_values[int(i % 4)][int(i / 4)]  # get correct number
                        if my_value == '=':
                            my_equation = str(round(eval(my_equation), 5))
                        else:
                            my_equation += my_value
                        delay_counter = 1

        # to avoid multiple clicks
        if delay_counter != 0:
            delay_counter += 1
            if delay_counter > 10:
                delay_counter = 0

        # Write the Final answer
        cv2.putText(img, my_equation, (810, 130), cv2.FONT_HERSHEY_PLAIN,
                    2, (0, 0, 0), 3)

        # Display
        key = cv2.waitKey(1)
        cv2.imshow("Image", img)
        if key == ord('c'):
            my_equation = ''


if __name__ == '__main__':
    main()
