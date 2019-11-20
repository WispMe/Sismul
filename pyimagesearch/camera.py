# import the necessary packages
from __future__ import print_function
from pyimagesearch.shapedetector import ShapeDetector
from PIL import Image
from PIL import ImageTk
import numpy as np
import tkinter as tki
import threading
import imutils
import cv2

class PhotoBoothApp:

    def __init__(self, window, vs, outputPath):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = window
        self.stopEvent = None
        self.shape = None

        # initialize the root window and image panel
        self.root = None
        self.panel = None

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()




    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading

        # threshold up and low din hsv
        lower = {'blue': (110, 100, 100), 'red': (-10, 100, 100), 'green': (40, 70, 70),
                 'yellow': (20, 100, 117)}  # assign new item lower['blue'] = (93, 10, 0)
        upper = {'blue': (130, 255, 255), 'red': (10, 255, 255), 'green': (70, 255, 255), 'yellow': (40, 255, 255)}


        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=640)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                blurred = cv2.GaussianBlur(self.frame, (11, 11), 0)
                image = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                # make a call for ShapeDetector class
                sd = ShapeDetector()

                # for each color in dictionary check object in frame
                for key, value in upper.items():
                    # construct a mask for the color from dictionary`1, then perform
                    # a series of dilations and erosions to remove any small
                    # blobs left in the mask
                    kernel = np.ones((9, 9), np.uint8)
                    mask = cv2.inRange(image, lower[key], upper[key])
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)

                    # find contours in the mask and initialize the current
                    # (x, y, w, h) center of the rectangle
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)[-2]
                    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                    center = None

                    # only proceed if at least one contour was found
                    if len(cnts) > 0:
                        # find the largest contour in the mask, then use
                        # it to compute the minimum enclosing circle and
                        # centroid
                        c = max(cnts, key=cv2.contourArea)
                        (x, y, w, h) = cv2.boundingRect(c)
                        M = cv2.moments(c)
                        if (M["m00"] == 0):
                            M["m00"] = 1
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                        if (x + y + w + h) > 400:
                            # Do when reach the minimum contours length
                            self.shape = sd.detect(c)
                            # c = c.astype("float")
                            c = c.astype("int")

                            if self.shape == "triangle":
                                cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
                                cv2.putText(image, self.shape, (x + 15, y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                          0.5, (255, 0, 0), 2)


                # Show image in GUI
                image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)


                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        # Stop the Thread
        self.stopEvent.set()

    def resume(self):
        # Resume the Thread
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()


