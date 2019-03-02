import cv2

# begin videostream()
class videostream:
    # the following method attempts to connect to the video source (computer camera)
    def __init__(self, videosource):
        self.VideoConnection = cv2.VideoCapture(videosource)
        if not self.VideoConnection.isOpened():
            raise ValueError("Cannot connect to video source", videosource)

        self.Width = self.VideoConnection.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.Height = self.VideoConnection.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # the following method returns a frame of the camera
    def getFrame(self):
        if self.VideoConnection.isOpened():
            ok, frame = self.VideoConnection.read()
            if ok:
                return (ok, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ok, None)
        else:
            return (ok, None)
    
    # the following method saves a frame from the video as a png image (no contours)
    def saveFrame(self):
        print("Saving Snapshot... Done")
        _, frame = self.VideoConnection.read()
        cv2.imwrite("Snapshot.png", frame)

    # the following method disconnects from the video source
    def release(self):
        if self.VideoConnection.isOpened():
            self.VideoConnection.release()
# end videostream()