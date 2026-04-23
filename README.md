# Firefighting_Game
This simple video game was adapted from a Tech With Tim tutorial (https://www.youtube.com/watch?v=waY3LfJhQLY). This is a passion project made for my partner who is a member of the fire service. The user plays as a firefighter who is tasked with putting out fires within several buildings that spawn at random. The number of fires and rate of spread are be determined by the user's selection of difficulty level (Easy, Medium, or Hard). The game ends when all the fires are put out, or when the fire extent becomes too large for the user to contain. 

### Class Requirements

For the final project, I have implemented classes to fulfill Task #1. I then incorporated user input (difficulty level selection) and utilized branching development (new-gameplay branch) to fulfill Task #2. 

### Installation
The use of conda (or mamba) is recommended to create a new environment using the provided `environment.yml` file:
```
git clone https://github.com/kamerritt/GEOS694_Final_Project_Game.git
cd GEOS694_Final_Project_Game
conda env create -f environment.yml
conda activate ff_game
```

### Current Version Information (v1.0.0)

The Firefighting Game only requires one script, `game.py`, that:

- Initializes the gameplay screen with the background `game_background.jpg`
- Provides the user an avatar `firefighter_transparent.jpg`
- Allows the user to move left and right and shoot water (space bar) (`water_transparent.png`) to put out fires (`flame_transparent.png`)
- Ends the game if a flame hits the avatar, or if all fires are extinguished

The game can be initiated with the following commands:
```                                                                             cd GEOS694_Final_Project_Game                                             
conda activate ff_game
python game.py                                                          
``` 
### Dependencies

This video game uses the following packages:

- pygame
- time
- random
- csv
  
