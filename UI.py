from Tkinter import *
import Tkinter as tk
#import drawAndSave as video
import cv2
from PIL import Image, ImageTk

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)




window = tk.Toplevel()
window.title("Settings")
#window.geometry('{}x{}'.format(300, 100))
Label(window, text="Resolution").grid(row=0, columnspan=2, sticky=W)
Label(window, text="X:").grid(row=1,sticky=W)
Label(window, text="Y:").grid(row=1, column=2,sticky=W)

x = StringVar(window, value='1280')
e1 = Entry(window, textvariable=x)

y = StringVar(window, value='720')
e2 = Entry(window, textvariable=y)


def callback():
    print "click!"
b = Button(window, text="Save", command=callback).grid(row = 1, column = 5, sticky = W)

e1.grid(row=1, column=1, pady = 10, padx = 15,sticky=W)
e2.grid(row=1, column=3, pady = 10, padx = 15,sticky=W)




show_frame()
root.mainloop()
