import math
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):
        return f"(vector({self.x},{self.y}))"


    def __repr__(self):
        return f"(vector:(x={self.x},y={self.y}))"


    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):
        #"""点积：(1,2)·(3,4) = 1*3 + 2*4 = 11"""
        return self.x * other.x + self.y * other.y

if __name__ == "__main__":
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(v1)            # vector(3,4)
    print(v1 + v2)       # vector(4,6)
    print(v1 - v2)       # vector(2,2)
    print(v2 * 3)        # vector(3,6)
    print(v1 == Vector(3, 4))  # True
    print(len(v1))       # 2
    print(v1[0])         # 3
    print(v1.length())   # 5.0
    print(v1.dot(v2))    # 11