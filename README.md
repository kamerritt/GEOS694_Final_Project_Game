# Firefighting_Game
This simple video game was adapted from a Tech With Tim tutorial (https://www.youtube.com/watch?v=waY3LfJhQLY). This is a passion project made for my partner who is a member of the fire service. The user plays as a firefighter who is tasked with putting out fires within several buildings that spawn at random. The number of fires and rate of spread will be determined by the user's selection of difficulty level (Easy, Medium, or Hard). The game ends when all the fires are put out, or when the fire extent becomes too large for the user to contain. 

### Class Requirements

For the final project, I will be choosing to make classes to fulfill Task #1. I will then be incorporating user input and utilizing branching development to fulfill Task #2. 

### Installation
*Install instructions for game conda environment.*
The use of conda (or mamba) is recommended to create a new environment using the provided `environment.yml` file:
```
git clone https://github.com/kamerritt/GEOS694_Final_Project_Game.git
cd GEOS694_Final_Project_Game
conda env create -f environment.yml
conda activate ff_game_env
```

### Current Version Information

The Firefighting Game only requires one script, `game.py`, that:

- Initializes the gameplay screen with the background `game_background.jpg`
- Provides the user an avatar `firefighter_transparent.jpg`
- Allows the user to move left and right and shoot water (`water_transparent.png`) to put out fires(`flame_transparent.png`)
- Ends the game if a flame hits the avatar, or if all fires are extinguished

### Dependencies

This video game uses the following packages:

- pygame
- time
- random
- csv
  
