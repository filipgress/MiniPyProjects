from tkinter import Tk, ttk, Button, StringVar 
from tkinter import *

WN_WIDTH = 250
WN_HEIGHT = 400

class SubWindow:
    windowCount = 0
    def __init__(self, body:'Body', window):
        from gravity import Body

        SubWindow.windowCount += 1

        self.body = body
        self.wn = Toplevel(window)
        self.wn.title("Edit - "+str(body.name))
        self.wn.geometry(str(WN_WIDTH)+'x'+str(WN_HEIGHT))

        self.wn.protocol("WM_DELETE_WINDOW", self.exit)

        label1 = ttk.Label(self.wn, text="Name")
        self.wn.name = StringVar(value=body.name)
        entry1 = ttk.Entry(self.wn, textvariable=self.wn.name)
        label1.pack()
        entry1.pack()

        label2 = ttk.Label(self.wn, text="Location X")
        self.wn.x_pos = StringVar(value=body.location.x)
        entry2 = ttk.Entry(self.wn, textvariable=self.wn.x_pos)
        label2.pack()
        entry2.pack()
        
        label3 = ttk.Label(self.wn, text="Location Y")
        self.wn.y_pos = StringVar(value=body.location.y)
        entry3 = ttk.Entry(self.wn, textvariable=self.wn.y_pos)
        label3.pack()
        entry3.pack()

        label4 = ttk.Label(self.wn, text="Mass")
        self.wn.mass = StringVar(value=body.mass)
        entry4 = ttk.Entry(self.wn, textvariable=self.wn.mass)
        label4.pack()
        entry4.pack()

        label5 = ttk.Label(self.wn, text="Motion vector X")
        self.wn.m_x = StringVar(value=body.motion_vector.x)
        entry5 = ttk.Entry(self.wn, textvariable=self.wn.m_x)
        label5.pack()
        entry5.pack()

        label6 = ttk.Label(self.wn, text="Motion vector Y")
        self.wn.m_y = StringVar(value=body.motion_vector.y)
        entry6 = ttk.Entry(self.wn, textvariable=self.wn.m_y)
        label6.pack()
        entry6.pack()

        button1 = Button(self.wn, text="Save", command=self.save)
        button2 = Button(self.wn, text="Exit", command=self.exit)
        button1.pack()
        button2.pack()

    def save(self):
        self.body.name = self.wn.name.get()
        self.body.location.x = float(self.wn.x_pos.get())
        self.body.location.y = float(self.wn.y_pos.get())

        self.body.mass = float(self.wn.mass.get())
        self.body.motion_vector.x = float(self.wn.m_x.get())
        self.body.motion_vector.y = float(self.wn.m_y.get())

        self.exit()

    
    def exit(self):
        self.wn.quit()
        self.wn.destroy()

        SubWindow.windowCount -= 1

