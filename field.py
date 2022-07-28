from pygame import Vector2
from tetramino import Tetramino


class Field:
    def __init__(self, width, height) -> None:
        self.width = width 
        self.height = height
        self.grid = [[-1 for _ in range(width)] for _ in range(height)]
    
    def add(self, tetramino: Tetramino) -> None:
        for square in tetramino.squares:
            self.grid[int(square.y)][int(square.x)] = tetramino.image

    def collide(self, square: Vector2) -> bool:
        y = max(int(square.y), 0)
        x = int(square.x)
        return self.grid[y][x] != -1
    
    def check_lines(self) -> int:
        lines = 0
        line = self.height - 1
        for y in range(self.height - 1, -1, -1):
            count = 0
            for x in range(self.width):
                if self.grid[y][x] != -1:
                    count += 1
                self.grid[line][x] = self.grid[y][x]
            if count < self.width:
                line -= 1
            else:
                lines += 1
        return lines
    
    def is_full(self) -> bool:
        return any(map(lambda x: x != -1, [self.grid[0][i] for i in range(3, 7)]))



