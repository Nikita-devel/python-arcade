"""
How-to-play text for every game, shown on the GUIDE screen.

Each variable below is a multi-line string. The menu reads these and draws
them line by line. Keeping all the instructions in one file means you can
fix a typo or improve wording without touching the game code at all.
"""

game_connect4 = """
Connect 4

Goal:
- Drop your pieces and be the first to line up four in a row —
  horizontally, vertically, or diagonally.

Controls:
- Move the mouse to pick a column.
- Left click to drop your piece into that column.

Turns:
- Player 1 is red, Player 2 is yellow. You take turns.

Game over:
- The game ends when someone gets four in a row, or the board fills up.
- A dialog asks if you want to play again.
"""

flappy_bird = """
Flappy Bird

Goal:
- Fly the bird through the gaps between the pipes and score points.

Controls:
- Press SPACE to flap and go up.
- Do nothing and gravity pulls you down.

Scoring:
- +1 point each time you pass through a gap.

Game over:
- You crash if you hit a pipe or the ground.
- Press SPACE to try again.
"""

pong_game = """
Pong

Goal:
- Bounce the ball past your opponent's paddle to score.

Controls:
- Left player:  'Z' up, 'S' down.
- Right player: UP arrow up, DOWN arrow down.
- Press ESC to quit.

Winning:
- First player to reach 7 points wins.
"""

snake_game = """
Snake

Goal:
- Eat the food to grow longer.
- Don't hit the walls or your own body.

Controls:
- Arrow keys to steer.
- 'Q' to quit, 'C' to play again after losing.

Scoring:
- Your score is your length. Beat your high score!
"""

space_shooter = """
Space Shooter

Goal:
- Survive waves of enemy ships and shoot them down.

Controls:
- Arrow keys (or W/A/S/D) to move your ship.
- SPACE to fire lasers.

Watch out:
- Enemies move down the screen. If they reach the bottom,
  or crash into you, you lose a life.
"""

aeroblaster = """
AeroBlaster

Goal:
- A fast-paced action shooter. Blast enemies and stay alive.

Controls:
- Arrow keys / A and D to move.
- SPACE (or the on-screen controls) to shoot and jump.

Tip:
- Keep moving — standing still makes you an easy target.
"""

gps_tool = """
GPS Data Analysis Tool

This one is a small utility, not a game.

How to use it:
1. Click "Démarrer" and choose a CSV file with GPS data.
2. Enter your average speed in meters per second.
3. Click "Analyser" to see the results:
   total distance, elevation gain/loss, max altitude,
   estimated travel time, and rough calories burned.

Note:
- Your CSV needs columns named "Distance (m)" and "Altitude (m)".
- Calorie numbers use a rough coefficient — treat them as estimates.
"""
