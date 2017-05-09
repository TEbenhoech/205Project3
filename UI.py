from Tkinter import *

window = Tk()
window.title("Settings")
#window.geometry('{}x{}'.format(300, 100))
Label(window, text="Resolution").grid(row=0, columnspan=2, sticky=W)
Label(window, text="X:").grid(row=1,sticky=W)
Label(window, text="Y:").grid(row=1, column=2,sticky=W)

x = StringVar(window, value='1280')
e1 = Entry(window, textvariable=x)

y = StringVar(window, value='720')
e2 = Entry(window, textvariable=y)

e1.grid(row=1, column=1, pady = 10, padx = 15,sticky=W)
e2.grid(row=1, column=3, pady = 10, padx = 15,sticky=W)

mainloop( )
