Wumpus World Game using PyGame Library
Python Wumpus World game created with Pygame. Hunt for gold while avoiding pits and the deadly Wumpus

Features:
- Grid-based Exploration: Navigate through an n×n grid cave system
- Multiple Difficulty Levels: Easy, Medium, and Hard modes with different attempt limits
- Sensory System: Detect nearby dangers through breeze, stench, and shine indicators
-  Arrow Mechanics: Limited arrows to hunt the Wumpus
- Score System: Points awarded for achievements and deducted for mistakes
- Visual Interface: Clean Pygame-based UI with HUD and popup notifications
- Customizable Grid Size: Configurable grid dimensions (3×3 to 8×8)
- Attempt System: Multiple lives based on difficulty level

How to Play:
1. Movement
- W/Up Arrow: Move up
- S/Down Arrow: Move down
- A/Left Arrow: Move left
-  D/Right Arrow: Move right
- ESC: Quit game

2. Shooting Arrows
- Click the arrow icon in the HUD
- Press a direction key to shoot in that direction
- Arrows travel in straight lines until hitting a wall or the Wumpus

3. Sensory Indicators
- Breeze: Indicates adjacent pits
- Stench: Indicates adjacent Wumpus
- Shine: Indicates adjacent gold

Game Scoring:
Starting Points: 1000
Movement: -1 point per move
Arrow Miss: -10 points
Wumpus Kill: +100 points
Gold Collection: +1000 points
Death: -1000 points