import pygame
from datetime import datetime 
pygame.init() 

class Clock(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        
        self.face = pygame.image.load('clock.png')
        self.Mickey = pygame.image.load('mickey.png')

    def draw_face(self, mx, my):
        pygame.Surface.set_colorkey(self.face, [255,255,255])
        DEFAULT_IMAGE_SIZE = (500, 500)
        self.face = pygame.transform.scale(self.face, DEFAULT_IMAGE_SIZE)
        screen.blit(self.face, (mx-250, my-250))

    def draw_mickey(self, mx, my):
        pygame.Surface.set_colorkey(self.Mickey, [255,255,255])
        self.Mickey = pygame.transform.scale(self.Mickey, (260,300))
        screen.blit(self.Mickey, (mx-130, my-150))

    class Minute_Arrow():
        def __init__(self):
            self.minute_arrow = pygame.image.load('minute_arrow.png').convert_alpha()
            
            

        def arrRotate(self, surf, pos, originPos, angle):
    
            image_rect = self.minute_arrow.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))

            offset = pygame.math.Vector2(image_rect.center) - pygame.math.Vector2(pos)

            rotated_offset = offset.rotate(-angle)

            rotated_center = pygame.math.Vector2(pos) + rotated_offset

            rotated_image = pygame.transform.rotate(self.minute_arrow, angle)
            rotated_rect = rotated_image.get_rect(center=rotated_center)

            surf.blit(rotated_image, rotated_rect)
    
    class Second_Arrow():
        def __init__(self):
            self.second_arrow = pygame.image.load('second_arrow.png').convert_alpha()

        def arrRotate(self, surf, pos, originPos, angle):
    
            image_rect = self.second_arrow.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))

            offset = pygame.math.Vector2(image_rect.center) - pygame.math.Vector2(pos)

            rotated_offset = offset.rotate(-angle)

            rotated_center = pygame.math.Vector2(pos) + rotated_offset

            rotated_image = pygame.transform.rotate(self.second_arrow, angle)
            rotated_rect = rotated_image.get_rect(center=rotated_center)

            surf.blit(rotated_image, rotated_rect)


SW, SH = 1000, 800
screen = pygame.display.set_mode((SW,SH))
clock = pygame.time.Clock()
run = True

Watch = Clock(screen)
Arrow1 = Watch.Minute_Arrow()
Arrow2 = Watch.Second_Arrow()

screen.fill((255,255,255))
mx, my = SW/2, SH/2
w1, h1 = Arrow1.minute_arrow.get_size()
w2, h2 = Arrow2.second_arrow.get_size()


while run:
    clock.tick(60)
    screen.fill((255,255,255))
    Watch.draw_mickey(mx, my)
    Watch.draw_face(mx, my)

    now = datetime.now()

    tm1 = now.minute * 6
    tm2 = now.second * 6
    
    Arrow1.arrRotate(
        screen,
        (mx, my),
        [w1/2, h1-20], -tm1)

    
    Arrow2.arrRotate(
        screen,
        (mx, my),
        [w2/2, h2-16], -tm2)
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
    

pygame.quit()