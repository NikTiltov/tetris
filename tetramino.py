from pygame import Vector2


class Tetramino:
    def __init__(self, index: int, image: int, pos: Vector2) -> None:
        self.squares = [Vector2(v) for v in types[index]]
        self.image = image
        self.move(pos)
    
    def move(self, vector):
        for square in self.squares:
            square += vector

    def rotate(self):
        center = self.squares[0]
        for square in self.squares:
            x = square.y - center.y
            y = square.x - center.x
            square.x = center.x - x
            square.y = center.y + y
            


types = [
    [(0, -1), (-1, -1), (-1, 0), (0,   0)],
    [(-1, 0), (-1,  1), (0,  0), (0,  -1)],
    [(0,  0), (-1,  0), (0,  1), (-1, -1)],
    [(0,  0), (0,  -1), (0,  1), (-1, -1)],
    [(-1, 0), (-2,  0), (0,  0), (1,   0)],
    [(0,  0), (0,  -1), (0,  1), (1,  -1)],
    [(0,  0), (0,  -1), (0,  1), (-1,  0)]
]