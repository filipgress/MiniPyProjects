from tkinter.messagebox import showinfo
from tkinter import Tk, ttk
from typing import List
from PIL import Image, ImageTk, ImageDraw

# x -- > lon
# y -- > lat

#  x     y	    lat                lon
# [192, 640] - [49.20981400000001, 16.598786]
# [606,  74] - [49.21762105,       16.60755785]

# 606 - 192 = 414
# 16.60755785 - 16.598786 = 0.00877185
# xz = 0.00877185 / 414 = 0.00002118804
 
# 640 - 74 = 566
# 49.20981400000001 - 49.21762105 = -0.00780704999
# yz = -0.00780704999 / 566 = -0.00001379337
 
# 16.598786 - 0.00002118804 * 191 = 16.5947390844
# 49.20981400000001 + 0.00001379337 * 639 = 49.2186279634

LONS =  16.5947390844  
LATS =  49.2186279634 
XZ   =  0.00002118804
YZ   = -0.00001379337

class Coord:
    def __init__(self, split: List[str]) -> None:
        decLon = self.convert(split[5], split[6])
        self.__x: int = 1+round((decLon - LONS)/XZ)

        decLat = self.convert(split[3], split[4])
        self.__y: int = 1+round((decLat - LATS)/YZ)

        self.__utc: float = float(split[1])

    def get_utc(self) -> float:
        return self.__utc
    def get_x(self) -> int:
        return self.__x
    def get_y(self) -> int:
        return self.__y

    def convert(self, coord: str, quadrant: str) -> float:
        dd = int(float(coord)/100)
        ss = float(coord) - dd * 100;
        dec = dd + ss/60;

        if quadrant == 'S' or quadrant == 'W':
            dec = -dec

        return dec

coords: List[Coord]=[]
valid: bool=True
def load(filepath: str) -> None:
    with open(filepath, "r") as file:
        for line in file.readlines():
            split = line.split(',')

            new_coord: Coord 
            if split[0] == "$GPRMC":
                if split[2] == 'A': # valid data
                    coords.append(Coord(split))
                else:
                    valid=False

def draw(filepath: str) -> None:
    with Image.open(filepath) as im:
        im = im.convert("RGB")
        draw = ImageDraw.Draw(im)

        for i in range(1, len(coords)):
            draw.line([(coords[i-1].get_x(), coords[i-1].get_y()), (coords[i].get_x(), coords[i].get_y())], fill="black", width=1)

        window = Tk()
        image = ImageTk.PhotoImage(im)
        label = ttk.Label(window, image=image)
        label.pack()
        im.save("test_map.gif")

        if not valid:
            showinfo('Error', "Some of the data corrupted!")

        window.mainloop()

FILE = "log.txt"
MAP = "map.gif"

if __name__ == "__main__":
    load(FILE)
    draw(MAP)
