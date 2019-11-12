from tkinter import *
from tkinter import filedialog
import threading
import time
from imutils.video import VideoStream
from pyimagesearch.detect_shapes import detectgambar


class tampilan:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tugas Sismul")
        self.root.geometry("180x120")
        self.kiri = Frame(self.root)
        self.kanan = Frame(self.root)

        #self.root.geometry("320x240")
        self.title = Label(self.root, text="TRIANGLE DETECTOR", font='Helvetica 10 bold')
        self.title.pack(pady=5)
        self.kiri.pack(side=LEFT)
        self.kanan.pack(side=RIGHT)

        #self.lokasi = Entry(self.kiri)
        #self.lokasi.pack(pady = 2)
        self.pilih = Button(self.kiri, text="Choose Image", command=self.openimage)
        self.pilih.pack(pady = 2)
        #self.detek = Button(self.kiri, text="Detect Image")
        #self.detek.pack(pady = 2)
        self.open = Button(self.kiri, text="Open Camera", command=self.opencamera)
        self.open.pack(side=TOP, pady=2)

    def openimage(self):
        filename = filedialog.askopenfilename()
        dg = detectgambar(filename)

    def opencamera(self):
        print("[INFO] warming up camera...")
        vs = VideoStream().start()
        time.sleep(2.0)

        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.shape = None

        self.stopEvent = threading.Event()
        self.thread = threading.Thread()
        self.thread.start()