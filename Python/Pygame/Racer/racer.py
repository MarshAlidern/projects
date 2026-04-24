import pygame, sys
from pygame.locals import *
import random, time
 

pygame.init()
 

FPS = 60
FramePerSec = pygame.time.Clock()
 

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SCORE = 0
COINS = 0

world_speed = 5
max_speed = 50
min_speed = 5

 

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("materials/AnimatedStreet.png")
road_y1 = 0
road_y2 = -SCREEN_HEIGHT
 

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("materials/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def update(self):
        global SCORE

        self.rect.y += world_speed * 1.3

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -20)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("materials/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed = pygame.key.get_pressed()

        if pressed[K_LEFT]:
            self.rect.x -= 5
        if pressed[K_RIGHT]:
            self.rect.x += 5

    
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))

class Coins(pygame.sprite.Sprite):
    def __init__(self, enemies_group):
        super().__init__()
        self.image = pygame.image.load("materials/coin.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        while True:
            self.rect.center = (
                random.randint(25, SCREEN_WIDTH - 25),
                random.randint(25, SCREEN_HEIGHT - 25)
            )

            if not pygame.sprite.spritecollideany(self, enemies_group):
                break

    def update(self):
        self.rect.y += world_speed


                   
     
P1 = Player()
E1 = Enemy()
 

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()


all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
 

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

pygame.mixer.init()

pygame.mixer.music.load('materials/Steamworks.mp3')
pygame.mixer.music.play()

coin_timer = 0

while True:
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        world_speed += 0.2
    else:
        world_speed -= 0.1
    world_speed = max(min_speed, min(max_speed, world_speed))

    coin_timer +=1
    if coin_timer > 60:  
        coin = Coins(enemies)
        coins.add(coin)
        all_sprites.add(coin)
        coin_timer = 0
    
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              world_speed += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    road_y1 += world_speed
    road_y2 += world_speed

    if road_y1 >= SCREEN_HEIGHT:
        road_y1 = -SCREEN_HEIGHT

    if road_y2 >= SCREEN_HEIGHT:
        road_y2 = -SCREEN_HEIGHT

    DISPLAYSURF.blit(background, (0, road_y1))
    DISPLAYSURF.blit(background, (0, road_y2))


    scores = font_small.render(f'SCORE: {SCORE}', True, BLACK)
    c_score = font_small.render(f'COINS: {COINS}', True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(c_score, (10,40))
 
    all_sprites.draw(DISPLAYSURF)
    all_sprites.update()
    

    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('materials/crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()

    hits = pygame.sprite.spritecollide(P1, coins, True)
    COINS+=len(hits)

         
    pygame.display.update()
    FramePerSec.tick(FPS)