import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (190, 190, 190)
RED = (200, 0, 30)

WIDTH = HEIGHT = 500
SQUARES = 20
SQUARE_SIZE = WIDTH // SQUARES # 10x10 board
OUTLINE = SQUARE_SIZE // 10
FPS = 30

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

class Snake:
        def __init__(self, head):
                self.body = []
                self.head = head
                self.just_grown = False

        def move(self, direction):
                x, y = self.head
                dx, dy = direction
                if len(self.body) != 0:
                        if not self.just_grown:
                                self.body.pop(0)
                        self.just_grown = False
                        self.body.append(self.head)
                else:
                        if self.just_grown:
                                self.body.append(self.head)
                                self.just_grown = False
                self.head = (x + dx, y + dy)

        def grow(self):
                self.just_grown = True

def init_window():
        win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("snake")

        return win

def draw_outlined_rect(win, color, x, y):
        pygame.draw.rect(win, color, (x * SQUARE_SIZE + OUTLINE, y * SQUARE_SIZE + OUTLINE, SQUARE_SIZE - OUTLINE * 2, SQUARE_SIZE - OUTLINE * 2))

def draw_screen(win, snake, apple):
        win.fill(BLACK)
        apple_x, apple_y = apple
        draw_outlined_rect(win, RED, apple_x, apple_y)

        for x, y in snake.body:
                draw_outlined_rect(win, WHITE, x, y)
        x, y = snake.head
        draw_outlined_rect(win, LIGHT_GREY, x, y)

def snake_out_of_borders(snake):
        x, y = snake.head
        return (x not in range(SQUARES)) or (y not in range(SQUARES))

def main():

        WIN = init_window()
        clock = pygame.time.Clock()
        run = True

        snake = Snake((SQUARES // 2 - 1, SQUARES // 2 - 1))
        apple = (SQUARES // 2, SQUARES // 2 - 1)
        direction = (0, 0)
        direction_unconfirmed = (0, 0)
        ticks = 0

        while run:
                clock.tick(FPS)

                if ticks == FPS // 4:
                        direction = direction_unconfirmed
                        snake.move(direction)
                        ticks = 0
                        direction_history = []

                ticks += 1

                for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                                run = False

                        elif e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_DOWN:
                                        if direction != UP:
                                                direction_unconfirmed = DOWN
                                elif e.key == pygame.K_UP:
                                        if direction != DOWN:
                                                direction_unconfirmed = UP
                                elif e.key == pygame.K_LEFT:
                                        if direction != RIGHT:
                                                direction_unconfirmed = LEFT
                                elif e.key == pygame.K_RIGHT:
                                        if direction != LEFT:
                                                direction_unconfirmed = RIGHT

                # checking the collisions
                if snake.head in snake.body or snake_out_of_borders(snake):
                        time.sleep(1)
                        run = False
                if snake.head == apple:
                        snake.grow()
                        x, y = random.randrange(SQUARES), random.randrange(SQUARES)
                        while (snake.head == (x, y)) or ((x, y) in snake.body):
                                x, y = random.randrange(SQUARES), random.randrange(SQUARES)
                        apple = (x, y)

                draw_screen(WIN, snake, apple)
                pygame.display.update()

if __name__ == "__main__":
        main()
