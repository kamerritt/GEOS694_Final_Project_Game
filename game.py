# Import packages
import pygame
import time
import random

# Initialize game and font
pygame.init()
pygame.font.init()

# Set gameplay window parameters and caption
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kyle Saves The Day!')

# Load and scale background, avatar, and fire images
BG = pygame.transform.scale(pygame.image.load('game_images/game_background.jpg'), (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load('game_images/firefighter_transparent.png').convert_alpha(), (100, 100))
FIRE_IMAGE = pygame.transform.scale(pygame.image.load('game_images/flame_transparent.png').convert_alpha(), (FIRE_WIDTH, FIRE_HEIGHT))

FONT = pygame.font.SysFont('comicsans', 30) # Set font type

class Avatar: 
    # Initialize avatar parameters 
    def __init__(self):
        self.rect = PLAYER_IMAGE.get_rect()
        self.rect.x = 200 # Starting location 
        self.rect.bottom = HEIGHT # Place on bottom of gameplay screen
        self.vel = 5 # Set velocity
    
    def move(self, keys):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x - self.vel >= 0:
            self.rect.x -= self.vel # Move avatar left with left arrow key press

        elif keys[pygame.K_RIGHT] and self.rect.x + self.vel + self.rect.width <= WIDTH:
            self.rect.x += self.vel # Move avatar right with right arrow key press

    def draw(self, WIN):
        WIN.blit(PLAYER_IMAGE, (self.rect.x, self.rect.y)) # Draw player on screen

        

# Function to draw items on gameplay screen 
def draw(player, time_elapsed, fires):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {round(time_elapsed)}s', 1, 'white') # Create gameplay clock
    WIN.blit(time_text, (10, 10))

    WIN.blit(PLAYER_IMAGE, (player.x, player.y)) # Draw avatar on screen

    for fire in fires:
        WIN.blit(FIRE_IMAGE, (fire.x, fire.y)) # Draw fire

    pygame.display.update() 

def main():
    run = True 

    # Place avatar on bottom of gameplay screen 
    player = PLAYER_IMAGE.get_rect()
    player.x = 200
    player.bottom = HEIGHT

    # Increase time on gameplay clock as long as run = True
    clock = pygame.time.Clock()
    starttime = time.time()
    time_elapsed = 0
    
    fire_add_increment = 2000 # Spawn new fires every 2000 milliseconds
    fire_count = 0 # Start game with zero fires

    fires = []
    hit = False

    while run:
        fire_count += clock.tick(60)
        time_elapsed = time.time() - starttime

        if fire_count > fire_add_increment:
            for i in range(3):
                fire_x = random.randint(0, WIDTH - FIRE_WIDTH)
                fire = pygame.Rect(fire_x, -FIRE_HEIGHT, FIRE_WIDTH, FIRE_HEIGHT)
                fires.append(fire) # Add fires to a random location on screen

                fire_add_increment = max(200, fire_add_increment - 50)
                fire_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Allow user to exit game
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL # Moves avatar left with left arrow key press

        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL  +player.width <= WIDTH:
            player.x += PLAYER_VEL # Moves avatar right with right arrow key press 

        for fire in fires[:]:
            fire.y += FIRE_VEL
            if fire.y > HEIGHT:
                fires.remove(fire)
            elif fire.y + fire.height >= player.y and fire.colliderect(player):
                fires.remove(fire)  
                hit = True # End game if avatar is hit by a flame
                break

        if hit:
            # Display 'You Lose' text and end game after 4000 milliseconds
            lost_text = FONT.render('You lost :(', 1, 'white') 
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, time_elapsed, fires)

    pygame.quit()


if __name__ == "__main__":
    main()