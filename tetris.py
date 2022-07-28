import pygame
from pygame import Vector2, Surface, Rect
from pygame import transform
from random import randint
from tetramino import Tetramino
from field import Field


FPS = 60
TILE = 7
WIDTH = 10
HEIGHT = 20
PIXEL_SIZE = Vector2(WIDTH * (TILE + 1) - 1, HEIGHT * (TILE + 1) - 1)
OFFSET = Vector2(8, 8)

pygame.init()
screen = pygame.display.set_mode(PIXEL_SIZE * 4 + OFFSET * 2)
image = Surface(PIXEL_SIZE)
clock = pygame.time.Clock()

squares = pygame.image.load("data/squares.png").convert()
rect = Rect((0, 0), (TILE, TILE))
images = []
for y in range(4):
        images.append([squares.subsurface(rect.move(TILE * x, TILE * y)) for x in range(4)])

font = pygame.font.Font("data/font.ttf", 8)

field = Field(WIDTH, HEIGHT)

time = 0
step = 1
exp = 0
level = 1000
mult = 1.2
acceleration = 0.7
image_index = 0

score = 0


def try_move(vector: Vector2) -> bool:
    tetramino.move(vector)
    if any(map(collide, tetramino.squares)):
        tetramino.move(-vector)
        return False
    return True


def try_rotate() -> bool:
    tetramino.rotate()
    if any(map(collide, tetramino.squares)):
        for _ in range(3):
            tetramino.rotate()
        return False
    return True


def collide(point: Vector2) -> bool:
    return point.x < 0 or point.x >= WIDTH or point.y >= 20 or field.collide(point)


def new_tetramino() -> Tetramino:
    return Tetramino(randint(0, 6), randint(0, 3), Vector2(5, -1))


tetramino = new_tetramino()

playing = True
running = True
while running:
    h_move = 0
    v_move = 0
    rotate = False
    down = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                h_move -= 1
            if event.key == pygame.K_RIGHT:
                h_move += 1
            if event.key == pygame.K_DOWN:
                v_move = 1
            if event.key == pygame.K_UP:
                rotate = True
            if event.key == pygame.K_SPACE:
                down = True
    
    if playing:
        try_move(Vector2(h_move, 0))

        time += 1 / FPS
        if time > step:
            time = 0
            v_move = 1
        
        if down:
            while try_move(Vector2(0, 1)):
                pass
        
        if rotate:
            try_rotate()

        if try_move(Vector2(0, v_move)) == False:
            field.add(tetramino)
            count = field.check_lines()
            if count > 0:
                score += 100 * 2 ** (count - 1)
                exp += 100 * 2 ** (count - 1)
                if exp > level:
                    exp = 0
                    level *= mult
                    step *= acceleration
                    image_index = (image_index + 1) % 4
            if field.is_full():
                playing = False
            tetramino = new_tetramino()

        square_image = images[image_index][tetramino.image]
        for square in tetramino.squares:
            image.blit(square_image, square * (TILE + 1))

        for y, row in enumerate(field.grid):
            for x, i in enumerate(row):
                if i != -1:
                    image.blit(images[image_index][i], (TILE * x + x, TILE * y + y))
    else:
        score_text = font.render("SCORE", False, "white")
        count_text = font.render(str(score), False, "white")
        image.blit(score_text, (10, 60))
        image.blit(count_text, (10, 70))
        

    screen.blit(transform.scale(image, PIXEL_SIZE * 4), OFFSET)
    pygame.display.update()
    image.fill("black")
    clock.tick(FPS)
    
pygame.quit()