import pygame

pygame.init()

RED = (255,0,0)
WHITE = (255,255,255)

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def clamp(self, w, h):
        self.x = max(self.radius, min(w - self.radius, self.x))
        self.y = max(self.radius, min(h - self.radius, self.y))


w, h = 1000, 800
screen = pygame.display.set_mode((w, h))
screen.fill(WHITE)
discription = pygame.display.set_caption('Officer BALLS')
clock = pygame.time.Clock()
ball = Ball(w/2, h/2, 25, RED)

run = True
v=10

while run:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        ball.move(-v, 0)
    if keys[pygame.K_d]:
        ball.move(v, 0)
    if keys[pygame.K_w]:
        ball.move(0, -v)
    if keys[pygame.K_s]:
        ball.move(0, v)
    ball.clamp(w,h)
    ball.draw(screen)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            
    
    clock.tick(60)
    pygame.display.update()

pygame.quit()