import pygame


pygame.init()

screen = pygame.display.set_mode()
screen.fill((255,255,255))
font = pygame.font.Font(None, 32)

run = True
btn_clicked = False
clock = pygame.time.Clock()


while run:
    btn_rect = pygame.Rect(100, 100, 200, 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click only
                if btn_rect.collidepoint(event.pos):
                    btn_clicked = True
                    click_time = pygame.time.get_ticks()


    mouse_pos = pygame.mouse.get_pos()
    if btn_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (100, 100, 255), btn_rect)
         
    else:
        pygame.draw.rect(screen, (0, 0, 255), btn_rect)

    if btn_clicked:
        elapsed = pygame.time.get_ticks() - click_time
        if elapsed > 2000:
            btn_clicked = False  # ← reset flag, text disappears
        else:
            text = font.render('Button is pressed!', True, (255, 255, 255))
            text_rect = text.get_rect(center=(btn_rect.centerx, btn_rect.centery))
            screen.blit(text, text_rect) 

    pygame.display.flip()
    clock.tick(60)   

pygame.quit()