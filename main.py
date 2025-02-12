import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MY Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 80)
game_active = True

sky_surface = pygame.image.load("graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

score_surface = test_font.render("Welcome to Jump World", False, (64, 64, 64))
score_rect = score_surface.get_rect(center=(400, 50))

snail_surface = pygame.image.load("graphics/snail/snail1.png")
snail_rect = snail_surface.get_rect(midbottom=(750, 300))

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:
                        player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom >= 300:
                        player_gravity = -20
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            snail_rect.left = 850



    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, "Red", score_rect, 6)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, -1)
        screen.blit(score_surface, score_rect)

        snail_rect.right -= 6
        if snail_rect.right < 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # PLAYER & FLOOR
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # COLLISIONS
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill("Orange")

    pygame.display.update()
    clock.tick(60)
