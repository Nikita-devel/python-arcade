import turtle  # Import the turtle library for the graphics
import time  # To cap the loop speed (see below)
import tkinter as tk  # Import tkinter for the pop-up dialogs
from tkinter import messagebox  # Import tkinter's message box
import pygame  # Import pygame to handle the sounds
import os  # Import the os module to handle file paths
from threading import Thread  # Import Thread to play the music in the background

# Set the working directory for the script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Start the pygame mixer
pygame.mixer.init()

# Load the sounds with os.path.join so the paths work on every platform
ball_bounce_sound = pygame.mixer.Sound(os.path.join(script_dir, "jump.wav"))
score_sound = pygame.mixer.Sound(os.path.join(script_dir,"scoree.wav"))
background_music = pygame.mixer.Sound(os.path.join(script_dir, "backgr.wav"))

# Function that plays background music in a separate thread
def play_background_music():
    background_music.play(-1)  # -1 indique la boucle infinie

# Start the background-music thread
bg_music_thread = Thread(target=play_background_music)
bg_music_thread.start()

wn = turtle.Screen()
wn.title("Pong par @Nikita")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
# The loop now runs at ~60 frames/second (see below). So the
# ball speed is a move PER FRAME, not "as fast
# as the CPU". 4 pixels/frame is fast but playable.
# Increase these to speed up, decrease them to slow down.
ball.dx = 4
ball.dy = -4

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Joueur A: 0 Joueur B: 0", align="center", font=("Courier", 24, "normal"))

# Function that plays the ball-bounce sound
def play_ball_bounce_sound():
    ball_bounce_sound.play()

# Function that plays the scoring sound
def play_score_sound():
    score_sound.play()

# Function that plays the background music
def play_background_music():
    background_music.play()

# Exit function
def exit_game():
    wn.bye()

# Check the win conditions
def check_win_conditions():
    global score_a, score_b
    if score_a == 7 or score_b == 7:
        winner = "Joueur A" if score_a == 7 else "Joueur B"
        response = messagebox.askquestion("Partie terminée", f"{winner} gagne !\nVoulez-vous rejouer ?")
        if response == "yes":
            reset_game()
        else:
            exit_game()

# Reset the game
def reset_game():
    global score_a, score_b
    score_a = 0
    score_b = 0
    pen.clear()
    pen.write("Joueur A: 0 Joueur B: 0", align="center", font=("Courier", 24, "normal"))
    paddle_a.goto(-350, 0)
    paddle_b.goto(350, 0)
    ball.goto(0, 0)
    ball.dx = 4
    ball.dy = -4

# Keyboard bindings for moving the paddles
wn.listen()
wn.onkeypress(lambda: paddle_a.sety(paddle_a.ycor() + 20), "z")
wn.onkeypress(lambda: paddle_a.sety(paddle_a.ycor() - 20), "s")
wn.onkeypress(lambda: paddle_b.sety(paddle_b.ycor() + 20), "Up")
wn.onkeypress(lambda: paddle_b.sety(paddle_b.ycor() - 20), "Down")
wn.onkeypress(exit_game, "Escape")  # Bouton de sortie

# Loop speed: we aim for 60 frames per second. This is what makes
# the game playable — without this cap the ball moved as fast as
# the CPU allowed (so, far too fast).
FPS = 60
frame_duration = 1 / FPS

# Main game loop.
# Everything is wrapped in try/except: when you close the window (X or
# the Esc key), turtle destroys its "canvas" but the loop was still
# drawing on it -> error "invalid command name .!canvas". We now catch
# that error (and the normal close) to exit cleanly.
try:
    while True:
        debut_image = time.time()
        wn.update()

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Collision with paddle A. Wide band + we check the ball is
        # going left (ball.dx < 0) to avoid double bounces.
        if -350 < ball.xcor() < -335 and ball.dx < 0 \
                and paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50:
            ball.setx(-335)
            ball.dx *= -1
            play_ball_bounce_sound()

        # Collision with paddle B (same idea, right side).
        if 335 < ball.xcor() < 350 and ball.dx > 0 \
                and paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50:
            ball.setx(335)
            ball.dx *= -1
            play_ball_bounce_sound()

        # Bounce off the top and bottom edges
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        # Point for player A (the ball leaves on the right)
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write("Joueur A: {} Joueur B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
            play_score_sound()
            check_win_conditions()

        # Point for player B (the ball leaves on the left)
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write("Joueur A: {} Joueur B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
            play_score_sound()
            check_win_conditions()

        # Cap at 60 frames/second: sleep for the rest of the frame.
        temps_ecoule = time.time() - debut_image
        reste = frame_duration - temps_ecoule
        if reste > 0:
            time.sleep(reste)

except (turtle.Terminator, tk.TclError):
    # The window was closed: we simply exit, with no error message.
    pass
