import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string

# begin Recog()
class Recog():
    # the following method process "Cutout.png" with pytesseract and returns the result as a string
    def readTextFromCutout(self):
        return pytesseract.image_to_string(Image.open("Cutout.png"))

    # the following method creates a series of images using the contours of the snapshot image
    # the images are as follows:
    # "Snapshot.png", "Contours.png", "Canvas.png", "Cropped.png", "Cutout.png"
    def processContoursForSnapshot(self):
        print("Begin Processing Snapshot... Done")
        snapshot = Image.open("Snapshot.png")
        snapshot.save("Snapshot.png", dpi=(300,300))
        snapshot = cv2.imread("Snapshot.png")
        snapshotCopy = snapshot.copy()

        # create a blank canvas
        canvas = np.zeros_like(snapshotCopy)

        # define the center rectangle
        x0 = round(1280*0.31)
        y0 = round(720*0.3)
        w0 = 484
        h0 = 285

        contours = self.findContourDataForImageFrame(snapshot)
        for c in contours:
            # obtain the perimeter of the contour
            # obtain the approximated shape of the contour
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1 * perimeter, True)

            # get the bounding rectangle
            x, y, w, h = cv2.boundingRect(c)

            # check to see if the perimeter is within these bounds
            if (perimeter > 400) and (perimeter < 1500):
                # draw the approximated shape with 4 vertices onto the copy of the snapshot in red
                # draw the bounding rectangle onto the copy of the snapshot in blue
                # draw the approximated shape with 4 vertices onto the blank canvas in white
                # draw the bounding rectangle onto the blank canvas in white
                if (len(approx) == 4):
                    cv2.drawContours(snapshotCopy, [approx], -1, (255, 0, 0), 3)
                    cv2.rectangle(snapshotCopy, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.drawContours(canvas, [approx], -1, (255, 255, 255), 3)
                    cv2.rectangle(canvas, (x, y), (x+w, y+h), (255, 255, 255), 3)
                else:
                    cv2.rectangle(snapshotCopy, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.rectangle(canvas, (x, y), (x+w, y+h), (255, 255, 255), 3)

        cv2.imwrite("Contours.png", snapshotCopy)
        cv2.imwrite("Canvas.png", canvas)

        # crop canvas to center rectangle
        cropped = canvas[y0:y0+h0, x0:x0+w0]
        cv2.imwrite("Cropped.png", cropped)

        # crop snapshot to center rectangle
        cutout = snapshot[y0:y0+h0, x0:x0+w0]
        cv2.imwrite("Cutout.png", cutout)

        secondContours = self.findContourDataForImageFrame(cropped)
        periMax = 0
        cMax = None
        for c in secondContours:
            # obtain the perimeter of the contour
            perimeter = cv2.arcLength(c, True)
            # check to find the max perimeter
            if perimeter > periMax:
                periMax = perimeter
                cMax = c
        
        # get the bounding rectangle for the contour with maximum perimeter
        # draw the bounding rectangle onto the cropped canvas in green
        # draw the bounding rectangle onto the cutout image in green
        x, y, w, h = cv2.boundingRect(cMax)
        cv2.rectangle(cropped, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.rectangle(cutout, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.imwrite("Cropped.png", cropped)
        cv2.imwrite("Cutout.png", cutout)

        # crop the cutout image to the boundary of the drawn green rectangle
        print("End Processing Snapshot... Done")
        secondCut = cutout[y:y+h, x:x+w]
        cv2.imwrite("Cutout.png", secondCut)

    # the following method finds the contours for the given image frame
    def findContourDataForImageFrame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)
        _, thresh = cv2.threshold(edged,127,255,0)
        _, contours, _ =  cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # the following method adds the contours to the given frame
    def getContourFrameForCameraFrame(self, frame):
        contours = self.findContourDataForImageFrame(frame)

        for c in contours:
            # obtain the perimeter of the contour
            # obtain the approximated shape of the contour
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1 * perimeter, True)

            # get the bounding rectangle
            x, y, w, h = cv2.boundingRect(c)

            # check to see if the perimeter is within these bounds
            if (perimeter > 400) and (perimeter < 1500):
                # draw the approximated shape with 4 vertices onto the frame in red
                # draw the bounding rectangle onto the frame in blue
                if (len(approx) == 4):
                    cv2.drawContours(frame, [approx], -1, (255, 0, 0), 3)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
            
        return frame
# end Recog()