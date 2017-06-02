from image_recognizer import Recognizer
import cv2
import imutils
from imutils import contours
from PIL import ImageGrab
import numpy as np


class GameDetector:
    def __init__(self):
        self.recognizer = Recognizer()
        self.recognizer.train()
        '''coordinates of the box'''
        '''mac dpi multiply location by 2'''
        self.score_box = (200 * 2, 333 * 2, 530 * 2, 356 * 2)
        self.box = (70 * 2, 308 * 2, 709 * 2, 709 * 2)
        self.predicted = []
        self.colors = []

    def is_end(self):
        # finding the end
        end_pil = ImageGrab.grab(self.box)
        end_np = np.array(end_pil)
        end_img = cv2.cvtColor(end_np, cv2.COLOR_BGR2RGB)
        end_1 = cv2.cvtColor(end_img, cv2.COLOR_BGR2GRAY)
        end_2 = cv2.threshold(end_1, 0, 255,
                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        end_3 = end_img.copy()

        cnts = cv2.findContours(end_2.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        max_area = -999
        max_loc = (0, 0, 0, 0)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if w * h > max_area:
                max_area = w * h
                max_loc = (x, y, w, h)

        (x, y, w, h) = max_loc
        cv2.rectangle(end_3, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # test the ratio of w to h
        if w * h > 300000 and abs(w / float(h) - 2) < .1:
            return True
        else:
            return False

    def get_score(self):
        # opencv segmentation
        img_pil = ImageGrab.grab(self.score_box)

        img_np = np.array(img_pil)
        img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        output = img.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # find contours in the thresholded image, then initialize the
        # digit contours lists
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        digits = []

        # loop over the digit area candidates
        cnts = contours.sort_contours(cnts, method="left-to-right")[0]

        is_neg = False

        dec_loc = (0, 0, 0, 0)

        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)

            # digits size
            if w >= 15 and h >= 40 and h <= 45:
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
                digits.append((x, y, w, h))
            elif w < 15 and h < 10:
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 1)
                dec_loc = (x, y, w, h)
            # negative distances
            elif w < 20 and h < 10 and cnts[0] is c:
                is_neg = True

        # svm to predict stuff
        numerator = 0
        denominator = 1

        for i in digits:
            (x, y, w, h) = i
            digit = img_pil.crop((x - 2, y - 2, x + w + 2, y + h + 2))
            # construct the number
            (x1, y1, w1, h1) = dec_loc
            if x > x1:
                denominator = denominator * 10
            numerator = numerator * 10 + self.recognizer.predict(digit)

        if is_neg:
            numerator = -numerator

        #error correction
        scr = numerator / float(denominator)

        test_mag = abs(scr) if abs(scr) < 5 else 5

        if len(self.predicted) > 0 and abs(self.predicted[-1] - scr) > test_mag:
            scr = self.predicted[-1]

        self.predicted.append(scr)
        return scr

    def new_game(self):
        self.predicted = []
