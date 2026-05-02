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

TASKS = {1: 40, 2: 60, 3: 80}

class Snake():
    def __init__(self):
        self.snake_body = [(COLS // 2, ROWS // 2)]
        self.direction = RIGHT
        self.next_dir = RIGHT
        self.speed = 0
        self.score = 0
        self.alive = True

    def update(self, food_pos):
        if not self.alive:
            return

        dx, dy = self.next_dir
        hx, hy = self.snake_body[0]
        new_head = (hx + dx, hy + dy)

        new_head = (new_head[0] % COLS, new_head[1] % ROWS)

        if new_head in self.snake_body:
            self.alive = False
            return

        self.direction = self.next_dir
        self.snake_body.insert(0, new_head)

        if new_head == food_pos:
            self.score += 10
            return True  
        else:
            self.snake_body.pop()
            return False


class Fruit():
    def __init__(self, snake):
        self.snake = snake
        self.pos = None
        self.mk_pos()

    def mk_pos(self):
        occupied = set(self.snake)
        while True:
            p = (random.randint(0, COLS - 1),
                 random.randint(0, ROWS - 1))
            if p not in occupied:
                self.pos = p
                break

    def new_pos(self):
        if self.pos in self.snake:
            self.mk_pos()


class GameState:
    def __init__(self):
        self.level = 1
        self.bg = BGL[1]
        self.level_timer = 0
        self.show_level = False
        self.overlay_type = None   
        self.free_mode = False


def chk_score(snake, state):
    if state.level in TASKS and snake.score >= TASKS[state.level]:
        state.level += 1
        snake.speed += 2
        state.show_level = True
        bg_key = min(state.level, max(BGL.keys()))
        state.bg = BGL[bg_key]
        state.level_timer = pygame.time.get_ticks()
        if state.level > max(TASKS.keys()):
            state.overlay_type = "congrats"


def cell_rect(x, y):
    return pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)


def draw_text(surf, text, size, x, y, color=TEXT_COL, anchor="center"):
    font = pygame.font.SysFont(None, size, bold=True)
    img = font.render(text, True, color)
    r = img.get_rect()
    setattr(r, anchor, (x, y))
    surf.blit(img, r)


def draw_grid(surf):
    for x in range(0, W, CELL):
        pygame.draw.line(surf, GRID_COL, (x, 0), (x, H))
    for y in range(0, H, CELL):
        pygame.draw.line(surf, GRID_COL, (0, y), (W, y))


def draw_game(surf, snk, frt_pos, bgc, scr):
    surf.fill(bgc)
    draw_grid(surf)
    fx, fy = frt_pos
    pygame.draw.rect(surf, FOOD_COL, cell_rect(fx, fy), border_radius=4)
    for i, (x, y) in enumerate(snk):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(surf, color, cell_rect(x, y), border_radius=4)

    draw_text(surf, f"SCORE {scr:04d}", 36,
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
    fruit = Fruit(snake.snake_body)

    status = GameState()
    started = False
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_q and status.overlay_type == "congrats":
                    status.overlay_type = None
                    status.free_mode = True
                    continue

                if event.key == pygame.K_r:
                    snake = Snake()
                    fruit = Fruit(snake.snake_body)
                    status = GameState()
                    started = False
                    continue

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
                    if not started and snake.alive:
                        started = True

                elif not snake.alive:
                    snake = Snake()
                    fruit = Fruit(snake.snake_body)
                    status = GameState()
                    started = False

        current_time = pygame.time.get_ticks()

        if status.overlay_type is None and started and snake.alive:
            ate = snake.update(fruit.pos)
            if ate:
                fruit.mk_pos()
                if not status.free_mode:
                    chk_score(snake, status)

            draw_game(screen, snake.snake_body, fruit.pos, status.bg, snake.score)

        if status.show_level:
            draw_overlay(screen, f"LEVEL {status.level}", "")
            if current_time - status.level_timer > 1500:
                status.show_level = False  

        if status.overlay_type == "congrats":
            draw_overlay(screen, "CONGRATS!", "R – restart   Q – free mode")
        elif status.free_mode:
            draw_text(screen, "FREE MODE", 24, 10, 10, color=DIM_COL, anchor="topleft")
        elif not started:
            draw_overlay(screen, "SNAKE", "Press arrow key to start")
        elif not snake.alive:

            draw_overlay(screen,
                         f"GAME OVER  {snake.score:04d}",
                         "Press any key to restart")

        pygame.display.flip()
        clock.tick(FPS + snake.speed)


if __name__ == "__main__":
    main()