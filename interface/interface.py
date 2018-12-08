from Tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
from .videostream import videostream
from recog.recog import ocrCard
from database import database

# begin TitanCardScannerApp()
class TitanCardScannerApp():
    # the following method initializes the main app window, connects to the camera, displays the video feed, and provides access to database
    def __init__(self):
        # create a main window called "TitanCard Scanner" with dimensions 500 x 410
        self.AppWindow = Tk()
        self.AppWindow.title("TitanCard Scanner")
        self.AppWindow.geometry('500x440')
        self.AppWindow.wm_protocol("WM_DELETE_WINDOW", self.__onCloseWindow__)

        # create a container in the main window for the video feed to be placed in
        self.VideoCanvas = Canvas(self.AppWindow, width=500, height=300, highlightthickness=0, relief='ridge')
        self.VideoCanvas.grid(row=1, column=1)

        # create a container to hold student information
        self.InfoCanvas = Canvas(self.AppWindow, width=20, height=5, highlightthickness=0, relief='ridge')
        self.InfoCanvas.grid(row=2, column=1)

        # create a container to hold name label and input field
        self.NameCanvas = Canvas(self.InfoCanvas, width=20, height=5, highlightthickness=0, relief='ridge')
        self.NameCanvas.grid(row=1, column=1)

        self.FirstNameLabel = Label(self.NameCanvas, text="Name")
        self.FirstNameLabel.grid(row=1, column=1)

        self.FirstNameEntryView = Entry(self.NameCanvas, width=20)
        self.FirstNameEntryView.grid(row=2, column=1)

        # create a container to hold id card label and input field
        self.TitanCardCanvas = Canvas(self.InfoCanvas, width=20, height=5, highlightthickness=0, relief='ridge')
        self.TitanCardCanvas.grid(row=1, column=2)

        self.TitanCardLabel = Label(self.TitanCardCanvas, text="CWID")
        self.TitanCardLabel.grid(row=1, column=1)

        self.TitanCardEntryView = Entry(self.TitanCardCanvas, width=10)
        self.TitanCardEntryView.grid(row=2, column=1)

        # create a container to hold email label and input field
        self.EmailCanvas = Canvas(self.InfoCanvas, width=20, height=5, highlightthickness=0, relief='ridge')
        self.EmailCanvas.grid(row=1, column=3)

        self.EmailLabel = Label(self.EmailCanvas, text="Email")
        self.EmailLabel.grid(row=1, column=1)

        self.EmailLabelEntryView = Entry(self.EmailCanvas, width=20)
        self.EmailLabelEntryView.grid(row=2, column=1)

        # create a container to hold buttons
        self.PrimaryButtonCanvas = Canvas(self.InfoCanvas, width=20, height=5, highlightthickness=0, relief='ridge')
        self.PrimaryButtonCanvas.grid(row=3, column=2)

        # for now, the following button checks if the person is subscribed to a club
        self.SignInButton = Button(self.PrimaryButtonCanvas, text='Sign In', command=self.__onClickSignInButton__)
        self.SignInButton.grid(row=1, column=1)

        # self.SubscribeButton = Button(self.PrimaryButtonCanvas, text='Subscribe', command=self.__onClickSubscribeButton__)
        # self.SubscribeButton.grid(row=1, column=1)

        # self.UnsubscribeButton = Button(self.PrimaryButtonCanvas, text='Unsubscribe', command=self.__onClickUnsubscribeButton__)
        # self.UnsubscribeButton.grid(row=1, column=1)

        self.ClearButton = Button(self.PrimaryButtonCanvas, text='Clear', command=self.__onClickClearButton__)
        self.ClearButton.grid(row=2, column=1)

        #
        self.SnapshotButton = Button(self.PrimaryButtonCanvas, text='Snapshot', command=self.__onClickSnapButton__)
        self.SnapshotButton.grid(row=3, column=1)

        # create variables that captures the video stream object and camera frames and display video
        self.CameraFrame = None
        self.VideoStream = videostream(0)
        self.displayVideo()

        # initialize database connection
        self.tcdb = database.TCDB()

        # display main app window
        self.AppWindow.mainloop()

    # the following method displays the video obtained from the video stream object
    # it is called continuously every 15 milliseconds
    def displayVideo(self):
        ok, self.CameraFrame = self.VideoStream.getFrame()

        if ok:
            self.Image = ImageTk.PhotoImage(image=Image.fromarray(self.CameraFrame))
            self.VideoCanvas.create_image(250,150,image=self.Image,anchor='center')

        self.CallID = self.AppWindow.after(15, self.displayVideo)

    # the following method checks if the person specified in the entry fields is subscribed to a club
    def __onClickSignInButton__(self):
        name = self.FirstNameEntryView.get()
        cwid = self.TitanCardEntryView.get()
        email = self.EmailLabelEntryView.get()
        person = (name, '0', cwid, email)
        if self.__isValidEntry__(person):
            if self.tcdb.isPersonSubscribedToClub(person):
                print(person[0]+" is subscribed to acmw")
            else:
                self.tcdb.subscribePersonToClub(person)
                print(person[0]+" is not subscribed to acmw")

    # the following method adds the person specified in the entry fields to the specified club
    # for now, the only club will be 'acmw'
    def __onClickSubscribeButton__(self):
        name = self.FirstNameEntryView.get()
        cwid = self.TitanCardEntryView.get()
        email = self.EmailLabelEntryView.get()
        person = (name, '0', cwid, email)
        if self.__isValidEntry__(person):
            print(person[0]+" has subscribed to acmw")
            self.tcdb.subscribePersonToClub(person)

    # the following method removes the person specified in the entry fields from the specified club
    # for now, the only club will be 'acmw'
    def __onClickUnsubscribeButton__(self):
        name = self.FirstNameEntryView.get()
        cwid = self.TitanCardEntryView.get()
        email = self.EmailLabelEntryView.get()
        person = (name, '0', cwid, email)
        if self.__isValidEntry__(person):
            if self.tcdb.isPersonSubscribedToClub(person):
                print(person[0]+" has unsubscribed from acmw")
                self.tcdb.unsubscribePersonFromClub(person)
            else:
                print(person[0]+" is not subscribed to acmw")

    # the following method clears the text in the input fields
    def __onClickClearButton__(self):
        self.FirstNameEntryView.delete(0,20)
        self.TitanCardEntryView.delete(0,10)
        self.EmailLabelEntryView.delete(0,20)

    def __onClickSnapButton__(self):
        ret, frame = self.VideoStream.VideoConnection.read()
        cv2.imwrite("cardcap.jpg", frame)
        print("Captured image, initiating OCR...")

        print(ocrCard())

    # the following method determines if the person tuple does not contain empty strings
    def __isValidEntry__(self, person):
        if person[0] == '':
            print("Invalid Name Entry")
            return False
        if person[2] == '':
            print("Invalid CWID Entry")
            return False
        if person[3] == '':
            print("Invalid Email Entry")
            return False
        return True

    # the following method stops the video stream and closes the application
    def __onCloseWindow__(self):
        print("Stopping Video... Done")
        self.AppWindow.after_cancel(self.CallID)
        print("Closing Video... Done")
        self.VideoStream.release()
        print("Closing Window... Done")
        self.AppWindow.quit()

# end TitanCardScannerApp()
