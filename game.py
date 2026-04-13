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
BG = pygame.transform.scale(pygame.image.load('game_images/game_background.jpg')
                            , (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.transform.smoothscale(pygame.image.load('game_images/' \
'firefighter_transparent.png').convert_alpha(), (100, 100))
FIRE_IMAGE = pygame.transform.smoothscale(pygame.image.load('game_images/' \
'flame_transparent.png').convert_alpha(), (30, 45))

FONT = pygame.font.SysFont('comicsans', 30) # Set font type

class Game:
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(image)
        self.window_locs = []

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y)) # Draw object on screen

class Avatar(Game): 
    def __init__(self):
        # Inherit self parameters from Game parent class
        super().__init__(PLAYER_IMAGE, 200, HEIGHT-100, 100, 100) 
        self.vel = 5 # Set avatar velocity
    
    def move(self, keys):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x - self.vel >= 0:
            self.rect.x -= self.vel # Move avatar left

        elif keys[pygame.K_RIGHT] and (self.rect.x + self.vel + 
                                       self.rect.width <= WIDTH):
            self.rect.x += self.vel # Move avatar right

    def draw(self, WIN):
        WIN.blit(PLAYER_IMAGE, (self.rect.x, self.rect.y)) # Draw player

class Fire(Game):
    def __init__(self):
        x = random.randint(0, WIDTH-30) # Spawn fire at random location
        # Inherit self parameters from Game parent class
        super().__init__(FIRE_IMAGE, x, -45, 30, 45) 
        self.vel = 3 # Set fire velocity

    def move(self):
        self.rect.y += self.vel # Fire moves down screen according to velocity
    
    def off_screen(self):
        return self.rect.y > HEIGHT # Fire moves off screen 
    
    def hit(self, avatar):
        # Allow for exact collisions between fire and avatar with mask shape
        dist = (self.rect.x - avatar.rect.x, self.rect.y - avatar.rect.y)
        return avatar.mask.overlap(self.mask, dist) is not None
    
class Play:
    def __init__(self):
        self.avatar = Avatar()
        self.fires = [] # Start off with zero fires

        self.clock = pygame.time.Clock() # Gameplay clock
        self.starttime = time.time()

        self.fire_add_increment = 2000 # Add fire every 2 seconds
        self.fire_count = 0
        self.window_locs = [] # Empty list of building locations for fire spawn

        self.run = True
        self.hit = False
        
    def spawn_fires(self):
        for i in range(3):
            self.fires.append(Fire()) # Add fire to list
        
        self.fire_add_increment = max(200, self.fire_add_increment-50)
        self.fire_count = 0
    
    def fire_location(self):
        for fire in self.fires[:]:
            fire.move()

            if fire.off_screen():
                self.fires.remove(fire) # Remove fire if off screen
            
            elif fire.hit(self.avatar):
                self.fires.remove(fire)
                self.hit = True # Change condition after avatar is hit
    
    # Draw objects on gameplay screen
    def draw(self):
        WIN.blit(BG, (0, 0)) # Draw background

        time_elapsed = time.time() - self.starttime
        time_text = FONT.render(f'Time: {round(time_elapsed)}s', 1, 'white')
        WIN.blit(time_text, (10, 10)) # Draw gameplay clock in upper left corner

        self.avatar.draw(WIN) # Draw avatar on screen

        for fire in self.fires:
            fire.draw(WIN) # Draw fires on screen
        
        pygame.display.update()

    
    def end_game(self):
        # If avatar is hit, game ends after 4 seconds of losing text
        lost_text = FONT.render('You Lost :(', 1, 'white')
        WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, 
        HEIGHT/2 - lost_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(4000)

    # Main function to run game
    def main(self):
        while self.run:
            self.fire_count += self.clock.tick(60) # Increase fire count

            # Spawn fires on screen until game ends
            if self.fire_count > self.fire_add_increment:
                self.spawn_fires()
            
            # End game if user clicks to exit screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()

                if loc not in self.window_locs:
                    self.window_locs.append(loc)


            # Allow avatar movement with key press
            keys = pygame.key.get_pressed()
            self.avatar.move(keys)

            self.fire_location() # Handle fires

            # End game if user is hit by fire
            if self.hit:
                self.end_game()
                break
                
            self.draw() # Draw all components until game ends

        print(self.window_locs)
        pygame.quit()

# Run game!
if __name__ == "__main__":
    play = Play()
    play.main()