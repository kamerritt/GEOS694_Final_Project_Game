# Import packages
import pygame
import time
import random
import csv

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
WATER_IMAGE = pygame.transform.smoothscale(pygame.image.load('game_images/' \
'water_transparent.png').convert_alpha(), (20, 35))

FONT = pygame.font.SysFont('comicsans', 50) # Set font type

class Game:
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = pygame.mask.from_surface(image)

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y)) # Draw object on screen

class Avatar(Game): 
    def __init__(self):
        self.original_image = PLAYER_IMAGE
        self.flipped_image = pygame.transform.flip(PLAYER_IMAGE, True, False)
        self.facing_right = False
        self.image = self.original_image
        # Inherit self parameters from Game parent class
        super().__init__(self.image, 200, HEIGHT-100, 100, 100) 
        self.vel = 5 # Set avatar velocity
    
    def move(self, keys):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.rect.x - self.vel >= -50:
            self.facing_right = False
            self.rect.x -= self.vel # Move avatar left

        elif keys[pygame.K_RIGHT] and (self.rect.x + self.vel + 
                                       self.rect.width <= WIDTH):
            self.facing_right = True
            self.rect.x += self.vel # Move avatar right
        
        # Update image and mask based on facing direction
        if self.facing_right:
            self.image = self.flipped_image
        else:
            self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Game):
    def __init__(self, x, y):
        rect = FIRE_IMAGE.get_rect(center=(x, y))
        # Inherit self parameters from parent class to spawn fires in windows
        super().__init__(FIRE_IMAGE, rect.x, rect.y, rect.width, rect.height) 
        self.vel = 0 # Set fire velocity

    def move(self):
        self.rect.y += self.vel # Fire moves down screen according to velocity
    
    def off_screen(self):
        return self.rect.y > HEIGHT # Fire moves off screen 
    
    def hit(self, avatar):
        # Allow for exact collisions between fire and avatar with mask shape
        dist = (self.rect.x - avatar.rect.x, self.rect.y - avatar.rect.y)
        return avatar.mask.overlap(self.mask, dist) is not None
    
class Water(Game):
    # Inherit self parameters from parent class
    def __init__(self, x, y):
        super().__init__(WATER_IMAGE, x, y, 10, 20)
        self.vel = -10
    
    def move(self):
        self.rect.y += self.vel

    def off_screen(self):
        return self.rect.y < 0

    def hit(self, fire): return self.rect.colliderect(fire.rect)
    
class Play:
    def __init__(self, spawn_time):
        self.avatar = Avatar()
        self.fires = [] # Start off with zero fires

        self.waters = []
        self.won = False

        self.clock = pygame.time.Clock() # Gameplay clock
        self.starttime = time.time()

        self.fire_add_increment = spawn_time # Add fire depending on difficulty
        self.fire_count = 0

        self.run = True
        self.hit = False

        self.spawned_once = False


        self.window_locs = []

        # Create a list of window locations for fire spawning
        with open('windows.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                x = int(row['x'].strip())
                y = int(row['y'].strip())
                self.window_locs.append((x, y))
        
    def spawn_fires(self):
        self.spawned_once = True
        for i in range(3):
            x, y = random.choice(self.window_locs)
            self.fires.append(Fire(x, y)) # Add fire to window
        
        self.fire_add_increment = max(200, self.fire_add_increment-50)
        self.fire_count = 0
    
    def fire_location(self):
        for fire in self.fires[:]:
            if fire.hit(self.avatar):
                self.fires.remove(fire)
                self.hit = True # Change condition after avatar is hit

    def shoot_water(self):
        for water in self.waters[:]:
            water.move()

            if water.off_screen():
                self.waters.remove(water)
                continue

            for fire in self.fires[:]:
                if water.hit(fire):
                    self.fires.remove(fire)
                    self.waters.remove(water)
                    break
    
    # Draw objects on gameplay screen
    def draw(self):
        WIN.blit(BG, (0, 0)) # Draw background

        time_elapsed = time.time() - self.starttime
        time_text = FONT.render(f'Time: {round(time_elapsed)}s', 1, 'white')
        WIN.blit(time_text, (10, 10)) # Draw gameplay clock in upper left corner

        self.avatar.draw(WIN) # Draw avatar on screen

        for fire in self.fires:
            fire.draw(WIN) # Draw fires on screen
        
        for water in self.waters:
            water.draw(WIN) # Draw water on screen 

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
            
            self.shoot_water() 
            
            # End game if user clicks to exit screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # Shoot water with space key
                        water = Water(self.avatar.rect.centerx, 
                                      self.avatar.rect.top)
                        self.waters.append(water)
                        

            # Allow avatar movement with key press
            keys = pygame.key.get_pressed()
            self.avatar.move(keys)

            self.fire_location() # Handle fires

            if self.spawned_once and len(self.fires) == 0:
                self.won = True

            # End game if user is hit by fire
            if self.hit:
                self.end_game()
                break
            
            if len(self.fires) > 20:
                self.hit = True

            if self.won: 
                self.win_screen()
                break    

            self.draw() # Draw all components until game ends

        #print(self.window_locs)
        pygame.quit()

# If all fires are put out, the user wins the game!
    def win_screen(self):
        win_text = FONT.render('You are a hero!', 1, 'white')
        WIN.blit(win_text, (
            WIDTH/2 - win_text.get_width()/2,
            HEIGHT/2 - win_text.get_height()/2
        ))

        pygame.display.update()
        pygame.time.delay(4000)

# Menu to select difficulty 
def menu():
    clock = pygame.time.Clock()
    while True:
        WIN.fill((0, 0, 0))

        title = FONT.render('Choose Difficulty', True, (255, 255, 255))
        easy = FONT.render('Press 1 - Easy', True, (0, 255, 0))
        medium = FONT.render('Press 2 - Medium', True, (255, 255, 0))
        hard = FONT.render ('Press 3 - Hard', True, (255, 0, 0))

        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        WIN.blit(easy, (WIDTH//2 - easy.get_width()//2, 320))
        WIN.blit(medium, (WIDTH//2 - medium.get_width()//2, 380))
        WIN.blit(hard, (WIDTH//2 - hard.get_width()//2, 440))

        pygame.display.update()
        clock.tick(60)

        # User presses 1 on keyboard for easy, 2 for medium, or 3 for hard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'easy'
                if event.key == pygame.K_2:
                    return 'medium'
                if event.key == pygame.K_3:
                    return 'hard'
                
def spawn_rate(difficulty):
    if difficulty == 'easy':
        return 3000
    elif difficulty == 'medium':
        return 2000
    elif difficulty == 'hard':
        return 1000

# Run game!
if __name__ == "__main__":
    difficulty = menu()
    if difficulty is None:
        pygame.quit()
        quit()
    
    spawn_time = spawn_rate(difficulty)
    play = Play(spawn_time)
    play.main()