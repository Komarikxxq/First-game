import pygame
import pygame as pg

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((750, 439))
pygame.display.set_caption('First gay')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
ghost = pg.transform.scale(pygame.image.load('images/ghost.png'), (60, 60)).convert_alpha()

theme = pygame.image.load('images/theme.png').convert()
walk_left = [
    pg.transform.scale(pygame.image.load('images/player_left1.png'), (70, 70)).convert_alpha(),
    pg.transform.scale(pygame.image.load('images/player_left2.png'), (70, 70)).convert_alpha(),
    pg.transform.scale(pygame.image.load('images/player_left1.png'), (70, 70)).convert_alpha(),
    pg.transform.scale(pygame.image.load('images/player_left3.png'), (70, 70)).convert_alpha(),
]
walk_right = [
    pg.transform.scale(pygame.image.load('images/player_right1.png'), (70, 70)).convert_alpha(),
    pg.transform.scale(pygame.image.load('images/player_right2.png'), (70, 70)).convert_alpha(),
    pg.transform.scale(pygame.image.load('images/player_right1.png'), (70, 70)).convert_alpha(),
    pg.transform.scale(pygame.image.load('images/player_right3.png'), (70, 70)).convert_alpha(),
]

player_anim_count = 0
theme_x = 0
ghost_list_in_game = []

player_speed = 8
player_x = 200
player_y = 300

is_jump = False
jump_count = 8

theme_sound = pygame.mixer.Sound('sounds/theme.mp3')
theme_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 7000)

gameplay = True

label = pygame.font.Font('fonts/MadimiOne-Regular.ttf', 40)
lose_label = label.render('You lose!', False, (193, 196, 199))
restart_label = label.render('Play again', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(300, 200))

bullets_left = 5
bullet = pg.transform.scale(pygame.image.load('images/bullet.png'), (10, 20)).convert_alpha()
bullets = []

running = True
while running:

    screen.blit(theme, (theme_x, 0))
    screen.blit(theme, (theme_x + 750, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 8

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 600:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        theme_x -= 5
        if theme_x == -750:
            theme_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 760:
                    bullets.pop(i)
                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (300, 100))
        bullets_left = 5
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 200
            ghost_list_in_game.clear()
            bullets.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(770, 300)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 70, player_y + 25)))
            bullets_left -= 1
    clock.tick(15)
