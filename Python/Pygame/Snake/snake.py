import pygame
import random
import sys

CELL = 20
COLS = 30
ROWS = 24
W, H = COLS * CELL, ROWS * CELL
FPS = 10

BGL = {
    1: (255, 171, 246),
    2: (227, 255, 181),
    3: (189, 252, 255)
}

GRID_COL  = (20, 24, 34)
SNAKE_HEAD = (80, 220, 120)
SNAKE_BODY = (40, 160, 80)
FOOD_COL  = (230, 70, 80)

TEXT_COL  = (200, 210, 220)
DIM_COL   = (80, 90, 110)

UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

Tasks = {1: 40, 2: 60, 3: 80}

def random_food(snake):
    occupied = set(snake)
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in occupied:
            return pos

class Snake():
    def __init__(self):
        self.snake_body = [(COLS // 2, ROWS // 2)]
        self.snake_head = self.snake_body[0]
        self.direction = RIGHT
        self.next_dir = RIGHT
        self.food = random_food(self.snake_body),
        self.score = 0
        self.alive = True
        self.level = 1
        self.speed = 0
        self.bg = BGL[1]
        self.show_level = False
        self.level_timer = 0
        self.overlay_type = None   
    
    def update(self):
        if self.alive:
            self.snake_body = [(COLS // 2, ROWS // 2)]

        dx, dy = self.next_dir
        hx, hy = self.snake_body[0]
        new_head = (hx + dx, hy + dy)

        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.alive = False


        if new_head in self.snake_body:
            self.alive = False


        self.direction = self.next_dir
        self.snake_body.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.food = random_food(self.snake_body)
        else:
            self.snake_body.pop()

def cell_rect(x, y):
    return pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)



def draw_text(surf, text, size, x, y, color=TEXT_COL, anchor="center"):
    font = pygame.font.SysFont(None, size, bold=True)
    img = font.render(text, True, color)
    r = img.get_rect()
    setattr(r, anchor, (x, y))
    surf.blit(img, r)


def chk_score(snake):
    if not snake.alive:
        return

    level = snake.level

    if snake.level >= Tasks[3]:
        snake.overlay_type = "congrats"
        return

    if level in Tasks and snake.score >= Tasks[level]:
        snake.score = 0
        snake.level += 1
        snake.speed += 2

        bg_index = (snake.level - 1) % len(BGL) + 1
        snake.bg = BGL[bg_index]

        snake.show_level = True
        snake.level_timer = pygame.time.get_ticks()

def draw_grid(surf):
    for x in range(0, W, CELL):
        pygame.draw.line(surf, GRID_COL, (x, 0), (x, H))
    for y in range(0, H, CELL):
        pygame.draw.line(surf, GRID_COL, (0, y), (W, y))

def draw_game(surf, snake):
    surf.fill(snake.bg)
    draw_grid(surf)

    fx, fy = snake.food
    pygame.draw.rect(surf, FOOD_COL, cell_rect(fx, fy), border_radius=4)

    for i, (x, y) in enumerate(snake.snake_body):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(surf, color, cell_rect(x, y), border_radius=4)

    draw_text(surf, f"SCORE {snake.score:04d}", 36,
              W - 10, 10, color=DIM_COL, anchor="topright")

def draw_overlay(surf, title, subtitle):
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surf.blit(overlay, (0, 0))
    draw_text(surf, title, 42, W//2, H//2 - 40)
    draw_text(surf, subtitle, 18, W//2, H//2 + 20, color=DIM_COL)

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    snake = Snake()

    started = False
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if snake.overlay_type == "congrats":
                    if event.key == pygame.K_r:
                        started = False

                elif event.key == pygame.K_r:
                    started = False

                elif not snake.alive:
                    started = False

                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    sys.exit()

                else:
                    key_dir = {
                        pygame.K_UP: UP,
                        pygame.K_w: UP,
                        pygame.K_DOWN: DOWN,
                        pygame.K_s: DOWN,
                        pygame.K_LEFT: LEFT,
                        pygame.K_a: LEFT,
                        pygame.K_RIGHT: RIGHT,
                        pygame.K_d: RIGHT,
                    }.get(event.key)

                    if key_dir and key_dir != OPPOSITES.get(snake.direction):
                        snake.next_dir = key_dir
                        started = True

        current_time = pygame.time.get_ticks()

        if snake.overlay_type is None and started and snake.alive:

            chk_score(snake)
            draw_game(screen,snake)

        if snake.show_level:
            draw_overlay(screen, f"LEVEL {snake.level}", "")

            if current_time - snake.level_timer > 1500:
                snake.level_timer = False

        if snake.overlay_type == "congrats":
            draw_overlay(screen, "CONGRATS!", "Press R to restart")

    
        if not started:
            draw_overlay(screen, "SNAKE", "Press key to start")
        elif not snake.alive:

            draw_overlay(screen,
                         f"GAME OVER {snake.level:04d}",
                         "Press any key")

        pygame.display.flip()
        clock.tick(FPS + snake.speed)


if __name__ == "__main__":
    main()