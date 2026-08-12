# Import the libraries we need
import pygame
import time
import random
import os

# Start up pygame
pygame.init()

# We start the sound system separately and guard it with try/except. On
# some computers (or with no sound card) pygame.mixer fails and used to
# crash the WHOLE game at startup. Now, if sound fails, the game still
# launches — just without sound.
son_actif = True
try:
    pygame.mixer.init()
except pygame.error:
    son_actif = False

# Define colors as RGB
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Get the folder this script lives in
base_path = os.path.dirname(os.path.abspath(__file__))

# Set up the game window
# Set up the game window.
# We do NOT force fullscreen with set_mode((0,0), FULLSCREEN): on
# some systems (Wayland especially) that call crashes SDL
# (segmentation fault). Instead we read the screen size with
# pygame.display.Info() and open a large normal window, a little
# smaller than the screen. This is stable everywhere.
_info = pygame.display.Info()
dis_width = min(1280, _info.current_w - 80)
dis_height = min(720, _info.current_h - 120)
dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('Jeu de serpent')

# Start pygame's clock
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 25

# Load the custom font
custom_font = pygame.font.Font(os.path.join(base_path, 'assets', 'font.ttf'), 25)

# Load the sound effects (guarded). If a sound file is missing or
# sound is unavailable, we simply turn sound off.
game_over_sound = None
eat_sound = None
if son_actif:
    try:
        game_over_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'gameover.mp3'))
        eat_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'eat.mp3'))
        pygame.mixer.music.load(os.path.join(base_path, 'audio', 'backsound.mp3'))
        pygame.mixer.music.play(-1)
    except pygame.error:
        son_actif = False

# Load the images
background_img = pygame.image.load(os.path.join(base_path, 'assets', 'background.jpg'))
snake_head_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets', 'Head.png')), (snake_block, snake_block))
snake_body_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets', 'Body.png')), (snake_block, snake_block))
food_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets', 'Food.png')), (snake_block, snake_block))

# Set up the angle and the game-over sound flag
angle = 0
global game_over_sound_played
game_over_sound_played = False

# Function that draws the score
def Your_score(score):
    value = custom_font.render("Votre score : " + str(score), True, yellow)
    dis.blit(value, [(dis_width - value.get_width()) // 2, 10])

# Function that draws a message
def message(msg, color):
    mesg = custom_font.render(msg, True, color)
    dis.blit(mesg, [(dis_width - mesg.get_width()) // 2, (dis_height - mesg.get_height()) // 2])

# Function that draws the snake
def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == 0:
            dis.blit(snake_head_img, (x[0], x[1]))
        else:
            dis.blit(snake_body_img, (x[0], x[1]))

# Function that spawns food
def spawn_food():
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    return foodx, foody

# Path to the file holding the high score
score_file_path = os.path.join(base_path, 'highest_score.txt')
highest_score = 0

# Function that loads the high score
def load_highest_score():
    global highest_score
    if os.path.exists(score_file_path):
        with open(score_file_path, 'r') as file:
            highest_score = int(file.read())

# Function that saves the high score
def save_highest_score():
    with open(score_file_path, 'w') as file:
        file.write(str(highest_score))

# Load the high score
load_highest_score()

# Function that draws the score
def show_score(score, record):
    score_text = custom_font.render(f"Score : {score} Record : {record}", True, yellow)
    dis.blit(score_text, [10, 10])

# Main game loop
def gameLoop():
    global game_over
    global game_over_sound_played
    global highest_score
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foods = [spawn_food() for _ in range(5)]

    while not game_over:
        while game_close == True:
            dis.blit(background_img, (0, 0))

            # Update the high score
            if Length_of_snake - 1 > highest_score:
                highest_score = Length_of_snake - 1
                save_highest_score()

            # Show the game-over message and the score
            message(f"Vous avez perdu ! Votre score : {Length_of_snake - 1} Score le plus élevé : {highest_score}", red)

            # Play the game-over sound if it hasn't played yet
            if not game_over_sound_played:
                if game_over_sound is not None:
                    game_over_sound.play()
                game_over_sound_played = True
            
            pygame.display.update()
            
            # Handle the player's key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Close the window
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        # We leave this game cleanly and return
                        # "restart". Before, gameLoop() called itself,
                        # which stacked games on top of each other
                        # (a source of bugs and crashes). An outer
                        # loop starts a fresh game instead.
                        game_over_sound_played = False
                        return "restart"

        # Handle the player's key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Handle collisions with the edges
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.blit(background_img, (0, 0))

        # Draw the food
        for food in foods:
            dis.blit(food_img, (food[0], food[1]))

        # Draw the snake and the score
        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1, highest_score)
        pygame.display.update()

        # Handle eating the food
        for food in foods:
            if x1 == food[0] and y1 == food[1]:
                foods.remove(food)
                foods.append(spawn_food())
                Length_of_snake += 1
                if eat_sound is not None:
                    eat_sound.play()

        # Update the snake head's position
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_List.insert(0, snake_Head)

        # Handle the snake's length
        if len(snake_List) > Length_of_snake:
            del snake_List[Length_of_snake:]

        # Handle collisions with the snake's own body
        for x in snake_List[1:]:
            if x == snake_Head:
                game_close = True

        clock.tick(snake_speed)

    # The game is over (the player pressed Q or closed the window).
    # We return "quit" to tell the outer loop to stop the game.
    save_highest_score()
    return "quit"


# Load the high score
load_highest_score()

# Outer loop: start a fresh game as long as the player presses
# 'C' (play again). As soon as a game returns "quit", we close.
# This is cleaner and safer than calling gameLoop() recursively.
while True:
    resultat = gameLoop()
    if resultat != "restart":
        break

if son_actif:
    pygame.mixer.music.stop()
pygame.quit()
