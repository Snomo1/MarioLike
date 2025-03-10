import random
from random import choice

import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("graphics/Audio/jump.mp3")
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -21
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_frame_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surface = test_font.render(f"Score:{current_time}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 6
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False):
        obstacles_group.empty()
        player.sprite.rect.bottom = 300
        player.sprite.gravity = 0
        return False
    else:
        return True


def player_animations():
    global player_surface, player_index
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MY Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("graphics/font/Pixeltype.ttf", 80)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("graphics/Audio/for momo naruto.mp3")
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

# SPRITE GROUPS
obstacles_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player.add(Player())

sky_surface = pygame.image.load("graphics/sky.png").convert_alpha()
sky_x_pos = 0
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()
ground_x_pos = 0

game_name_surface = test_font.render("JUMPTOPIA", False, "#0959c5")
game_name_rect = game_name_surface.get_rect(center=(400, 40))

# Menu Texts
guide_surface = test_font.render("Press                    to Jump", False, "#0959c5")
guide_rect = guide_surface.get_rect(center=(400, 360))
guide_surface2 = test_font.render("SPACE", False, "Yellow")
guide_rect2 = guide_surface2.get_rect(center=(380, 360))
guide_surface3 = test_font.render("  to \nStart ", False, "#0959c5")
guide_surface3 = pygame.transform.rotozoom(guide_surface3, 0, 0.8)
guide_rect3 = guide_surface3.get_rect(center=(630, 150))
guide_surface4 = test_font.render("TAB", False, "Yellow")
guide_rect4 = guide_surface4.get_rect(center=(530, 130))

# Obstacle_list
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frame = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frame[snail_frame_index]

# snail_rect = snail_surface.get_rect(midbottom=(750, 300))
fly_frame_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
fly_frame = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frame[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0
# Intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= 300:
                        player_gravity = -21

            if event.type == obstacle_timer:
                obstacles_group.add(Obstacles(choice(["fly", "fly", "snail", "snail","snail"])))
                # if randint(0, 2):
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1500), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1500), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frame[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frame[fly_frame_index]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom >= 300:
                        player_gravity = -21
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            game_active = True
            # snail_rect.left = 850
            start_time = pygame.time.get_ticks()

    if game_active:
        # screen.blit(sky_surface, (0, 0))
        # THIS IS WHERE I MADE CHANGES TO THE BACKGROUND AND FLOOR ANIMATION
        sky_x_pos -= 1  # Move the background left
        if sky_x_pos <= -800:  # Reset when it fully moves out
            sky_x_pos = 0

        screen.blit(sky_surface, (sky_x_pos, 0))
        screen.blit(sky_surface, (sky_x_pos + 800, 0))  # Second copy for seamless looping

        # screen.blit(ground_surface, (0, 300))
        ground_x_pos -= 3
        if ground_x_pos <= - 800:
            ground_x_pos = 0
        screen.blit(ground_surface, (ground_x_pos, 300))
        screen.blit(ground_surface, (ground_x_pos + 800, 300))
        # pygame.draw.rect(screen, "Red", score_rect, 6)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, -1)

        score = display_score()

        # snail_rect.right -= 6
        # if snail_rect.right < 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # PLAYER & FLOOR
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animations()
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update()
        obstacles_group.draw(screen)
        obstacles_group.update()

        # OBSTACLE movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # COLLISIONS

        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        game_active = collision_sprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name_surface, game_name_rect)
        obstacle_rect_list.clear()
        player_rect.bottom = 300
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, "#e87a08")
        score_message_rect = score_message.get_rect(center=(400, 310))
        if score == 0:
            screen.blit(guide_surface, guide_rect) and \
            screen.blit(guide_surface2, guide_rect2) and \
            screen.blit(guide_surface3, guide_rect3) and \
            screen.blit(guide_surface4, guide_rect4)
        else:
            screen.blit(score_message, score_message_rect) and \
            screen.blit(guide_surface, guide_rect) and \
            screen.blit(guide_surface2, guide_rect2) and \
            screen.blit(guide_surface3, guide_rect3) and \
            screen.blit(guide_surface4, guide_rect4)

    pygame.display.update()
    clock.tick(60)
