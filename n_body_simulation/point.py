import math

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"({round(self.x, 2)}, {round(self.y, 2)})"
    
    __repr__ = __str__

    def __add__(self, b: 'Point'):
        return Point(self.x + b.x, self.y + b.y)

    def __sub__(self, b: 'Point'):
        return Point(self.x - b.x, self.y - b.y)

    def __mul__(self, b: float):
        return Point(self.x * b, self.y * b)

    def distance(self, b: 'Point') -> float:
        distance_in_x_and_y_axis = self - b
        return math.sqrt(distance_in_x_and_y_axis.x**2 + distance_in_x_and_y_axis.y**2)


Vector = Point  # alias

if __name__ == "__main__":
    examples()
