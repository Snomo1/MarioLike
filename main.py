import pygame
from sys import exit
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("MY Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("graphics/font/Pixeltype.ttf",80)

sky_surface = pygame.image.load("graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

score_surface = test_font.render("Welcome to Jump World",False,(64,64,64))
score_rect = score_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load("graphics/snail/snail1.png")
snail_rect = snail_surface.get_rect(midbottom = (750,300))

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos)
        #     if player_rect.collidepoint(event.pos):
        #         print("Boom")

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen,"#c0e8ec",score_rect,15)
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    #pygame.draw.line(screen,"Black",(0,0),pygame.mouse.get_pos(),5)
    #pygame.draw.ellipse(screen,"Red",pygame.Rect(500,200,50,150),5)

    screen.blit(score_surface, score_rect)
    screen.blit(player_surface, player_rect)

    snail_rect.right -= 4
    if snail_rect.right < 0:
        snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    # if player_rect.colliderect(snail_rect):
    #     print("Collision")

    pygame.display.update()
    clock.tick(60)