from tkinter import Tk, ttk, Canvas
from turtle import TurtleScreen
from turtle import RawTurtle
from time import time
from point import Point, Vector

import math

WN_SIZE = 600

G = 6.67430 * 10**(-11)
MASS = 10**7

class Body:
    def __init__(self, pos: Point, mass: float, 
                 motion_vec: Vector, screen: TurtleScreen):
        self.pos = self.turtlePos(pos)
        self.mass = mass
        self.motionVec = motion_vec 

        # turtle
        self.tr = RawTurtle(screen)
        self.tr.shape("circle")
        self.tr.shapesize(0.6, 0.6)

        clr = 'red' if mass > 0 else 'blue'
        self.tr.color(clr)

        # set first pos
        self.tr.up()
        self.tr.goto(self.pos.x, self.pos.y)
        self.tr.down()

    def turtlePos(self, pos: Point) -> Point:
        xPos = pos.x - WN_SIZE / 2
        yPos = pos.y - WN_SIZE / 2

        return Point(xPos, -yPos)

    def update(self, bodies: list['Body'], dt: float) -> None:
        if self.mass <= 0:
            return None

        for body in bodies:
            if body is self:
                continue

            diff = body.pos - self.pos
            dist = math.sqrt(diff.x**2 + diff.y**2)

            if dist < 3:
                self.mass = 0
                self.motionVec = Vector(0, 0)
                self.tr.color('black')
                continue

            force = G * dt * body.mass / dist**3

            self.motionVec.x += force * diff.x
            self.motionVec.y += force * diff.y

    def move(self, dt: float) -> None:
        self.pos += self.motionVec * dt
        self.tr.goto(self.pos.x, self.pos.y)

class App:
    def __init__(self):
        self.bodies: list[Body] = []
        self.running = True

        # window
        self.root = Tk()
        self.root.title("N-Body simulation")

        self.canvas = Canvas(self.root, width = WN_SIZE, height = WN_SIZE)
        self.canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
        self.canvas.pack()

        self.screen = TurtleScreen(self.canvas)
        self.screen.tracer(False)

        self.label = ttk.Label(self.root, 
                               text="c - erase, left-click - positive, right-click - negative");
        self.label.pack();

        # events
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind('c', self.erase)
        self.canvas.bind("<Button-1>", self.onLClick)
        self.canvas.bind("<Button-3>", self.onRClick)

    def onLClick(self, clickPos):
        self.bodies.append(Body(clickPos, MASS, Vector(0, 0), self.screen))

    def onRClick(self, clickPos):
        self.bodies.append(Body(clickPos, -MASS, Vector(0, 0), self.screen))

    def erase(self, e = 0):
        self.bodies.clear()
        self.canvas.delete('all')

    def isOut(self, body: Body) -> bool:
        half = WN_SIZE / 2 - 10
        return body.pos.x > half or body.pos.x < -half or\
        body.pos.y > half or body.pos.y < -half

    def run(self):
        start = time()

        while self.running:
            dt = time() - start

            for body in self.bodies:
                body.update(self.bodies, dt)
                body.move(dt)

                if self.isOut(body):
                    self.bodies.remove(body)

            self.screen.update()
            self.root.update()

    def close(self):
        self.running = False

if __name__ == '__main__':
    app = App()
    app.run()

