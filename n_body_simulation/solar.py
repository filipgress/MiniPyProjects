from typing import List, Optional
from tkinter import Tk, ttk, Canvas, Button, StringVar
from turtle import TurtleScreen

from gravity import Body, calculate_system_energy
from initial_states import solar_bodies, n_nary_stable_system
from window import SubWindow
from point import Point, Vector

WN_SIZE = 600

class App:
    def __init__(self):
        self.running = True
        self.paused = False

        self.master = Tk()
        self.master.title("N-Body simulation")
        Body.window = self.master

        self.canvas = Canvas(self.master, width = WN_SIZE, height = WN_SIZE)
        self.canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
        self.canvas.pack()

        self.screen = TurtleScreen(self.canvas)
        self.screen.tracer(False)
        Body.screen = self.screen

        self.multiple = 1
        self.step_size = 10**4
        self.con_step = self.convert_sec(self.step_size)

        self.bodies = solar_bodies(only_first_n_planets=9)
        for body in self.bodies: 
            body.goto() # set initial positions

        self.button = Button(self.master, text="Play/Pause", command=self.pause)
        self.button.pack()

        self.variable1 = StringVar()
        self.label1 = ttk.Label(self.master, textvariable=self.variable1)
        self.label1.pack()

        self.label2 = ttk.Label(self.master, text="Keyboard shortcuts: Play/Pause - SPACE | Slow-down: Q | Speed-up E\n"\
                +"Wipe star trails: R | Remove all Turtles: C | Click on Turtle to edit\n"\
                +"SHIFT + Click on empty space to create new Turtle")
        self.label2.pack()

        # events
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.bind('e', self.speedUp)
        self.master.bind('q', self.slowDown)
        self.master.bind("<space>", self.pause)
        self.master.bind('r', self.clear)
        self.master.bind('c', self.delete)
        self.canvas.bind("<Shift-1>", self.newBody)

    def newBody(self, event):
        position = Point((event.x - WN_SIZE/2)*Body.scale, -(event.y-WN_SIZE/2)*Body.scale)
        mass = 10**27
        motion_vector = Point(1200, 8000)
        name = "new_body"

        body = Body(position, mass, motion_vector, name)
        wn = SubWindow(body, self.master)

        body.goto()
        self.bodies.append(body)

    def speedUp(self, event):
        self.multiple += 1

    def slowDown(self, event):
        if self.multiple > 1:
            self.multiple -= 1

    def clear(self, event=0):
        for body in self.bodies:
            body.tr.clear()

    def delete(self, event):
        self.bodies.clear()
        self.canvas.delete('all')

    def pause(self, event=0):
        self.paused = not self.paused

    def close(self):
        self.running = False

    def convert_sec(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)

        return str(y)+" years, "+str(d)+" days, "+str(h)+" hours, "+str(m)+" minumtes, "+str(s)+" seconds"

    def mainloop(self):
        step_id = 0
        elapsed_time = 0

        initial_energy_level = calculate_system_energy(self.bodies)
        while self.running:
            if not self.paused and SubWindow.windowCount == 0:
                for body in self.bodies:
                    body.update(self.bodies, self.step_size*self.multiple)
                    body.move(self.step_size*self.multiple)

                step_id += 1
                elapsed_time += self.step_size*self.multiple


            string: str() = ""
            string += "Step ID: "+str(step_id)
            string += " | Elapsed time: "+str(self.convert_sec(elapsed_time))
            string += "\nStep size: "+self.con_step
            string += " | Steps per update: "+str(self.multiple)

            self.variable1.set(string)
            self.master.update()
            self.screen.update()

        print(calculate_system_energy(self.bodies) / initial_energy_level * 100)


if __name__ == '__main__':
    app = App()
    app.mainloop()

