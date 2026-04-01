import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kyle Saves The Day!')

BG = pygame.image.load('game_images/game_background.jpg')
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

PLAYER_IMAGE = pygame.image.load('game_images/firefighter_transparent.png').convert_alpha()
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
#PLAYER_RECT = PLAYER_IMAGE.get_rect(center=())

PLAYER_VEL = 5

FIRE_IMAGE = pygame.image.load('game_images/flame_transparent.png').convert_alpha()
FIRE_WIDTH = 30
FIRE_HEIGHT = 45
FIRE_VEL = 3
FIRE_IMAGE = pygame.transform.scale(FIRE_IMAGE, (FIRE_WIDTH, FIRE_HEIGHT))

FONT = pygame.font.SysFont('comicsans', 30)

def draw(player, time_elapsed, fires):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {round(time_elapsed)}s', 1, 'white')
    WIN.blit(time_text, (10, 10))

    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    for fire in fires:
        WIN.blit(FIRE_IMAGE, (fire.x, fire.y))

    pygame.display.update() 

def main():
    run = True

    #player = pygame.Rect(200, (HEIGHT - PLAYER_HEIGHT), PLAYER_WIDTH, PLAYER_HEIGHT)
    player = PLAYER_IMAGE.get_rect()
    player.x = 200
    player.bottom = HEIGHT

    clock = pygame.time.Clock()
    starttime = time.time()
    time_elapsed = 0
    
    fire_add_increment = 2000
    fire_count = 0

    fires = []
    hit = False

    while run:
        fire_count += clock.tick(60)
        time_elapsed = time.time() - starttime

        if fire_count > fire_add_increment:
            for i in range(3):
                fire_x = random.randint(0, WIDTH - FIRE_WIDTH)
                fire = pygame.Rect(fire_x, -FIRE_HEIGHT, FIRE_WIDTH, FIRE_HEIGHT)
                fires.append(fire)

                fire_add_increment = max(200, fire_add_increment - 50)
                fire_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL  +player.width <= WIDTH:
            player.x += PLAYER_VEL   

        for fire in fires[:]:
            fire.y += FIRE_VEL
            if fire.y > HEIGHT:
                fires.remove(fire)
            elif fire.y + fire.height >= player.y and fire.colliderect(player):
                fires.remove(fire)  
                hit = True
                break

        if hit:
            lost_text = FONT.render('You lost :(', 1, 'white')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, time_elapsed, fires)

    pygame.quit()


if __name__ == "__main__":
    main()