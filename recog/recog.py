import cv2
import numpy as np
from PIL import Image
from pytesseract import image_to_string

# begin Recog()
class Recog():
    # the following method process "Cutout.png" with pytesseract and returns the result as a string
    def readTextFromCutout(self):
        return image_to_string(Image.open("Cutout.png"))

    # the following method creates a series of images using the contours of the snapshot image
    # the images are as follows:
    # "Core-Snapshot.png", "Contours.png", "Canvas.png", "Cropped.png", "Cutout.png"
    def processContoursForSnapshot(self):
        print("Begin Processing Snapshot... Done")
        snapshot = Image.open("Core-Snapshot.png")
        snapshot.save("Core-Snapshot.png", dpi=(300,300))
        snapshot = cv2.imread("Core-Snapshot.png")
        snapshotCopy = snapshot.copy()

        # create a blank canvas
        canvas = np.zeros_like(snapshotCopy)

        # define the center rectangle
        x0 = int(round(1280*0.31))
        y0 = int(round(720*0.3))
        w0 = 484
        h0 = 285

        contours = self.findContourDataForImageFrame(snapshot)
        for c in contours:
            # get the bounding rectangle and its center point
            x, y, w, h = cv2.boundingRect(c)
            mx = int(x+w/2)
            my = int(y+h/2)

            # draw the contour onto the snapshot in green
            # draw the contour onto the blank canvas in white
            # check to see if the bounding rectangle's center lies in the bounds of the center rectangle
            # if so: draw the bounding rectangle onto the snapshot in blue
            # and: draw the bounding rectangle onto the blank canvas in white
            cv2.drawContours(snapshotCopy, [c], -1, (0, 255, 0), 3)
            cv2.drawContours(canvas, [c], -1, (255, 255, 255), 3)
            if (mx > x0) and (mx < x0 + w0) and (my > y0) and (my < y0 + h0):
                cv2.rectangle(snapshotCopy, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.rectangle(canvas, (x, y), (x+w, y+h), (255, 255, 255), 3)

        cv2.imwrite("Contours.png", snapshotCopy)
        cv2.imwrite("Canvas.png", canvas)

        # crop canvas to center rectangle
        cropped = canvas[y0:y0+h0, x0:x0+w0]
        cv2.imwrite("Cropped.png", cropped)

        # crop snapshot to center rectangle
        cutout = snapshot[int(y0):int(y0+h0), int(x0):int(x0+w0)]
        cv2.imwrite("Cutout.png", cutout)

        secondContours = self.findContourDataForImageFrame(cropped)
        perimeters = []
        boundingRectangles = {}
        for c in secondContours:
            # obtain the perimeter of the contour and the bounding rectangle
            perimeter = cv2.arcLength(c, True)
            x, y, w, h = cv2.boundingRect(c)
            
            # create a key-value pair with the perimeter as the key and the bounding rectangle dimensions as the value
            kv = {perimeter:(x,y,w,h)}

            # save the perimeter value into a list
            # save the bounding rectangles dictionary with the key-value pair
            perimeters.append(perimeter)
            boundingRectangles.update(kv)
        
        # obtain the largest perimeter
        perimeterMax = max(perimeters)

        # get the bounding rectangle for the contour with maximum perimeter
        # draw the bounding rectangle onto the cropped canvas in green
        # draw the bounding rectangle onto the cutout image in green
        x, y, w, h = boundingRectangles.pop(perimeterMax)
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
        _, thresh = cv2.threshold(edged, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    # the following method adds the contours to the given frame
    def getContourFrameForCameraFrame(self, frame):
        # define the center rectangle
        x0 = int(round(1280*0.31))
        y0 = int(round(720*0.3))
        w0 = 484
        h0 = 285

        contours = self.findContourDataForImageFrame(frame)
        for c in contours:
            # get the bounding rectangle and its center point
            x, y, w, h = cv2.boundingRect(c)
            mx = int(x+w/2)
            my = int(y+h/2)

            # draw the contour onto the frame in green
            # check to see if the bounding rectangle's center lies in the bounds of the center rectangle
            # if so: draw the bounding rectangle onto the frame in blue
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 3)
            if (mx > x0) and (mx < x0 + w0) and (my > y0) and (my < y0 + h0):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
        
        return frame
# end Recog()
