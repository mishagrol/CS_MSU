import numpy as np


class Atom:
    def __init__(self, _type="Ag", x=1, y=1, z=1):
        self.type = _type
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Atom):
            return Atom(self.type, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if isinstance(other, Atom):
            return Atom(self.type, self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __str__(self):
        return f"X: {self.x}\tY: {self.y}\tZ: {self.z}"

    def transform(self, tansformation):
        return Atom(
            self.type,
            self.x * tansformation[0] + self.y * tansformation[1] + self.z * tansformation[2],
            self.x * tansformation[3] + self.y * tansformation[4] + self.z * tansformation[5],
            self.x * tansformation[6] + self.y * tansformation[7] + self.z * tansformation[8]
        )

    def distance(self):
        return np.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

