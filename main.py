import pygame
from sys import exit


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surface = test_font.render(f"Score:{current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MY Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 80)
game_active = False
start_time = 0

sky_surface = pygame.image.load("graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

game_name_surface = test_font.render("JUMPTOPIA", False, ("Blue"))
game_name_rect = game_name_surface.get_rect(center=(400, 40))

guide_surface = test_font.render("Press                    to Jump", False, (64, 64, 64))
guide_rect = guide_surface.get_rect(center=(400, 360))
guide_surface2 = test_font.render("SPACE", False, ("Yellow"))
guide_rect2 = guide_surface2.get_rect(center=(380, 360))


snail_surface = pygame.image.load("graphics/snail/snail1.png")
snail_rect = snail_surface.get_rect(midbottom=(750, 300))

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))

#Intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))


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
            start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, "Red", score_rect, 6)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, -1)

        display_score()

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
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(guide_surface,guide_rect)
        screen.blit(guide_surface2, guide_rect2)
        screen.blit(game_name_surface,game_name_rect)



    pygame.display.update()
    clock.tick(60)
