import pygame
import os

pygame.init()
pygame.mixer.init()

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (100, 100, 100)
GREEN  = (0,   200, 0)
RED    = (200, 0,   0)
BLUE   = (0,   100, 255)
YELLOW = (255,196,12)
ORANGE = (255,   100, 0)


screen = pygame.display.set_mode((650, 200), pygame.RESIZABLE)
pygame.display.set_caption('Music Player')
Icon = pygame.image.load('1.png')
Icon = pygame.transform.scale(Icon, (32, 32))  # force 32x32
pygame.display.set_icon(Icon)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)


volume = 1.0
paused = False

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)
    label = font.render(text, True, WHITE)
    lx = x + (w - label.get_width()) // 2
    ly = y + (h - label.get_height()) // 2
    screen.blit(label, (lx, ly))
    return pygame.Rect(x, y, w, h)

path = os.getcwd()
songs = [f for f in os.listdir(path) if f.lower().endswith(('.mp3', '.wav', '.flac'))]

current = 0

if songs:
    pygame.mixer.music.load(os.path.join(path, songs[current]))
    pygame.mixer.music.play()
else:
    print("Нет аудиофайлов в папке!")


running = True
while running:
    screen.fill(WHITE)

    # --- draw buttons ---
    play_btn  = draw_button('Play',  30,  80, 100, 50, GREEN)
    pause_btn = draw_button('Pause', 150, 80, 100, 50, BLUE)
    stop_btn  = draw_button('Stop',  270, 80, 100, 50, RED)
    nxt_btn  = draw_button('Next',  390, 80, 100, 50, YELLOW)
    prv_btn  = draw_button('Prev',  510, 80, 100, 50, ORANGE)


    pygame.draw.rect(screen, GRAY, (30, 160, 600, 20), border_radius=10)

    pygame.draw.rect(screen, GREEN, (30, 160, int(600 * volume), 20), border_radius=10)

    name_text = font.render(songs[current], True, BLACK)
    vol_text = font.render(f'Volume: {int(volume * 100)}%', True, BLACK)
    screen.blit(name_text, (30, 10))
    screen.blit(vol_text, (30, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

  
            if play_btn.collidepoint(mx, my):
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.play(-1)

            if pause_btn.collidepoint(mx, my):
                if not paused:
                    pygame.mixer.music.pause()
                    paused = True

            if stop_btn.collidepoint(mx, my):
                pygame.mixer.music.stop()
                paused = False
            
            if nxt_btn.collidepoint(event.pos):
                current = (current + 1) % len(songs)
                pygame.mixer.music.load(os.path.join(path, songs[current]))
                pygame.mixer.music.play()

            if prv_btn.collidepoint(event.pos):
                current = (current - 1) % len(songs)
                pygame.mixer.music.load(os.path.join(path, songs[current]))
                pygame.mixer.music.play()

            if 30 <= mx <= 630 and 150 <= my <= 180:
                volume = (mx - 30) / 600
                pygame.mixer.music.set_volume(volume)


        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  
                mx, my = event.pos
                if 30 <= mx <= 630 and 140 <= my <= 190:
                    volume = (mx - 30) / 600
                    volume = max(0.0, min(1.0, volume))  
                    pygame.mixer.music.set_volume(volume)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()