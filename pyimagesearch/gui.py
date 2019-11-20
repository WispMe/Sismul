from tkinter import *
from tkinter import filedialog
from imutils.video import VideoStream
from pyimagesearch.detect_shapes import detectgambar
from pyimagesearch.camera import PhotoBoothApp
import time



class tampilan:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tugas Sismul")
        self.root.geometry("240x120")
        self.kiri = Frame(self.root)
        self.kanan = Frame(self.root)

        #self.root.geometry("320x240")
        self.title = Label(self.root, text="TRIANGLE DETECTOR", font='Helvetica 10 bold')
        self.title.pack(pady=5)
        self.kiri.pack(side=TOP)
        self.kanan.pack(side=RIGHT)

        #self.lokasi = Entry(self.kiri)
        #self.lokasi.pack(pady = 2)
        self.pilih = Button(self.kiri, text="Choose Image", command=self.openimage)
        self.pilih.pack(pady = 2)
        #self.detek = Button(self.kiri, text="Detect Image")
        #self.detek.pack(pady = 2)
        self.open = Button(self.kiri, text="Open Camera", command=self.opencamera)
        self.open.pack(pady=2)

    def openimage(self):
        filename = filedialog.askopenfilename()
        dg = detectgambar(filename)

    def opencamera(self):
        print("[INFO] warming up camera...")
        self.root.geometry("640x480")

        vs = VideoStream(usePiCamera="").start()
        time.sleep(2.0)

        # Create a window and pass it to the Application object
        PhotoBoothApp(Toplevel(self.root), vs, "output")


