import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kyle Saves The Day!')

BG = pygame.image.load('/Users/kamerritt/Desktop/game/game_background.jpg')
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

FIRE_WIDTH = 10
FIRE_HEIGHT = 20
FIRE_VEL = 3

FONT = pygame.font.SysFont('comicsans', 30)

def draw(player, time_elapsed, fires):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {round(time_elapsed)}s', 1, 'white')
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, 'green', player)

    for fire in fires:
        pygame.draw.rect(WIN, 'red', fire)

    pygame.display.update() 

def main():
    run = True

    player = pygame.Rect(200, (HEIGHT - PLAYER_HEIGHT), PLAYER_WIDTH, PLAYER_HEIGHT)

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

    pygame.quit


if __name__ == "__main__":
    main()