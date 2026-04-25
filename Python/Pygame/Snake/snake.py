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
SNAKE_HEAD= (80, 220, 120)
SNAKE_BODY= (40, 160, 80)
FOOD_COL  = (230, 70, 80)

TEXT_COL  = (200, 210, 220)
DIM_COL   = (80, 90, 110)

UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)

OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

Tasks = {1: 40, 2: 60, 3: 80}

def cell_rect(x, y):
    return pygame.Rect(x * CELL + 1, y * CELL + 1, CELL - 2, CELL - 2)

def random_food(snake):
    occupied = set(snake)
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in occupied:
            return pos

def draw_text(surf, text, size, x, y, color=TEXT_COL, anchor="center"):
    font = pygame.font.SysFont(None, size, bold=True)
    img = font.render(text, True, color)
    r = img.get_rect()
    setattr(r, anchor, (x, y))
    surf.blit(img, r)

def new_game():
    start = (COLS // 2, ROWS // 2)
    snake = [start, (start[0]-1, start[1]), (start[0]-2, start[1])]

    return {
        "snake": snake,
        "direction": RIGHT,
        "next_dir": RIGHT,
        "food": random_food(snake),
        "score": 0,
        "alive": True,

        "level": 1,
        "speed": 0,
        "bg": BGL[1],

        "show_level": False,
        "level_timer": 0,

        "overlay_type": None   
    }

def update(state):
    if not state["alive"]:
        return state

    dx, dy = state["next_dir"]
    hx, hy = state["snake"][0]
    new_head = (hx + dx, hy + dy)

    if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
        state["alive"] = False
        return state

    if new_head in state["snake"]:
        state["alive"] = False
        return state

    state["direction"] = state["next_dir"]
    state["snake"].insert(0, new_head)

    if new_head == state["food"]:
        state["score"] += 10
        state["food"] = random_food(state["snake"])
    else:
        state["snake"].pop()

    return state

def chk_score(state):
    if not state["alive"]:
        return

    level = state["level"]

    if state["score"] >= Tasks[3]:
        state["overlay_type"] = "congrats"
        return

    if level in Tasks and state["score"] >= Tasks[level]:
        state["level"] += 1
        state["speed"] += 2

        bg_index = (state["level"] - 1) % len(BGL) + 1
        state["bg"] = BGL[bg_index]

        state["show_level"] = True
        state["level_timer"] = pygame.time.get_ticks()

def draw_grid(surf):
    for x in range(0, W, CELL):
        pygame.draw.line(surf, GRID_COL, (x, 0), (x, H))
    for y in range(0, H, CELL):
        pygame.draw.line(surf, GRID_COL, (0, y), (W, y))

def draw_game(surf, state):
    surf.fill(state["bg"])
    draw_grid(surf)

    fx, fy = state["food"]
    pygame.draw.rect(surf, FOOD_COL, cell_rect(fx, fy), border_radius=4)

    for i, (x, y) in enumerate(state["snake"]):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(surf, color, cell_rect(x, y), border_radius=4)

    draw_text(surf, f"SCORE {state['score']:04d}", 18,
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

    state = new_game()
    started = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if state["overlay_type"] == "congrats":
                    if event.key == pygame.K_r:
                        state = new_game()
                        started = False

                elif event.key == pygame.K_r:
                    state = new_game()
                    started = False

                elif not state["alive"]:
                    state = new_game()
                    started = False

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

                    if key_dir and key_dir != OPPOSITES.get(state["direction"]):
                        state["next_dir"] = key_dir
                        started = True

        current_time = pygame.time.get_ticks()

        if state["overlay_type"] is None and started and state["alive"]:
            state = update(state)

        chk_score(state)

        draw_game(screen, state)

        if state["show_level"]:
            draw_overlay(screen, f"LEVEL {state['level']}", "")

            if current_time - state["level_timer"] > 1500:
                state["show_level"] = False

        if state["overlay_type"] == "congrats":
            draw_overlay(screen, "CONGRATS!", "Press R to restart")

    
        if not started:
            draw_overlay(screen, "SNAKE", "Press key to start")
        elif not state["alive"]:
            draw_overlay(screen,
                         f"GAME OVER {state['score']:04d}",
                         "Press any key")

        pygame.display.flip()
        clock.tick(FPS + state["speed"])


if __name__ == "__main__":
    main()