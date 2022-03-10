class Interval:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a + other.a, self.b + other.b)
        else:
            raise TypeError("Must be interval")

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a - other.b, self.b - other.a)
        else:
            raise TypeError("Must be interval")

    def __mul__(self, other):
        if isinstance(other, Interval):
            return Interval(
                min(self.a * other.a, self.a * other.b, self.b * other.a, self.b * other.b),
                max(self.a * other.a, self.a * other.b, self.b * other.a, self.b * other.b)
            )
        else:
            raise TypeError("Must be interval")

    def __truediv__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a, self.b) * Interval(1 / other.b, 1 / other.a)
        else:
            raise TypeError("Must be interval")

    def __floordiv__(self, other):
        if isinstance(other, Interval):
            return Interval(self.a, self.b) * Interval(1 / other.b, 1 / other.a)
        else:
            raise TypeError("Must be interval")

    def __str__(self):
        return f"[{self.a}, {self.b}]"

    def __repr__(self):
        return f"[{self.a}, {self.b}]"
