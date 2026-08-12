"""
Main menu for the Python Arcade.

This is the program you run first. It shows a fullscreen menu with three
buttons: PROGRAMS (the list of games), GUIDE (how to play each game), and
QUIT. When you click a game, this file starts that game in a separate
Python process, waits for it to finish, then brings you back to the menu.

Beginner note:
    A "process" is just a running program. Instead of importing every game
    into this file (which would be messy and could crash the menu if one
    game has a bug), we launch each game the same way you would from a
    terminal: `python path/to/game.py`. If a game crashes, only that
    process dies, and the menu stays alive.

Run it with:
    python main.py
"""

import sys
import os
import logging
import subprocess

import pygame

from menu_lib.button import Button
from menu_lib.explanations import (
    flappy_bird,
    game_connect4,
    gps_tool,
    pong_game,
    snake_game,
    space_shooter,
    aeroblaster,
)

# --- Setup -----------------------------------------------------------------

# pygame.init() turns on all of pygame's modules (graphics, fonts, etc.).
# pygame.mixer.init() turns on the sound system specifically.
pygame.init()
pygame.mixer.init()

# Logging lets us print helpful error messages with a timestamp instead of
# letting the program crash silently. We use it below when loading sounds.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# base_path is the folder this file lives in. We build every other path
# from it (with os.path.join) so the program works no matter which folder
# you run it from. Never hard-code paths like "C:/Users/..." — they break
# on other computers.
base_path = os.path.dirname(os.path.abspath(__file__))


def asset(*parts):
    """Build a full path to a file inside the assets/ folder.

    Example: asset("audio", "click_sound.mp3")
    returns something like ".../assets/audio/click_sound.mp3".
    """
    return os.path.join(base_path, "assets", *parts)


# --- Load sounds -----------------------------------------------------------
# We wrap each load in try/except. If a sound file is missing, we log the
# error and keep going instead of crashing the whole menu. A missing click
# sound should not stop you from playing games.

background_music = None
click_sound = None

try:
    background_music = pygame.mixer.Sound(asset("audio", "mainbgs.mp3"))
    background_music.set_volume(0.4)
    background_music.play(-1)  # -1 means "loop forever".
except pygame.error as error:
    logging.error("Could not load background music: %s", error)

try:
    click_sound = pygame.mixer.Sound(asset("audio", "click_sound.mp3"))
    # Volume goes from 0.0 (silent) to 1.0 (full). Values above 1.0 are
    # ignored, so we use 1.0, not 2.
    click_sound.set_volume(1.0)
except pygame.error as error:
    logging.error("Could not load click sound: %s", error)


def play_click():
    """Play the click sound, but only if it loaded successfully."""
    if click_sound is not None:
        click_sound.play()


# --- Screen setup ----------------------------------------------------------

# (0, 0) + FULLSCREEN tells pygame to use the whole monitor at its native
# resolution. We then read that resolution back so we can center things.
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()

# Load the background image once and scale it to fill the screen.
BG = pygame.image.load(asset("Background.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))


def get_font(size):
    """Return the custom game font at the requested size (in pixels)."""
    return pygame.font.Font(asset("font.ttf"), size)


# How many items to show on one page of the PROGRAMS / GUIDE lists.
GAMES_PER_PAGE = 5


# --- The game catalogue ----------------------------------------------------
# One list, used by both the PROGRAMS screen (to launch games) and the
# GUIDE screen (to show instructions). Keeping it in one place means you
# only edit it once when you add a new game.

GAMES = [
    {"name": "Puissance 4", "path": "games/connect4/connect4.py", "explanation": game_connect4},
    {"name": "Flappy Bird", "path": "games/flappy-bird/flappy.py", "explanation": flappy_bird},
    {"name": "GPS Analyse", "path": "games/gps/gps_csv.py", "explanation": gps_tool},
    {"name": "Beta Minecraft", "path": "games/minecraft/minecraft.py",
     "explanation": "Look around with the mouse, walk with WASD.\n"
                    "Left click removes a block, right click adds one.\n"
                    "Press 'P' to quit."},
    {"name": "Pong Game", "path": "games/pong/pong_game.py", "explanation": pong_game},
    {"name": "Snake", "path": "games/snake/snake_game.py", "explanation": snake_game},
    {"name": "Space Shooter", "path": "games/SpaceShooter/main.py", "explanation": space_shooter},
    {"name": "AeroBlaster", "path": "games/AeroblasterSource/Aeroblaster.py", "explanation": aeroblaster},
]


def launch_game(relative_path):
    """Start a game in its own process and pause the menu music.

    We use sys.executable (the exact Python that is running this menu)
    instead of the string "python". On some computers the command is
    "python3", or "python" points at the wrong version — sys.executable
    always points at the right one.
    """
    try:
        if background_music is not None:
            background_music.stop()

        full_path = os.path.join(base_path, relative_path)
        game_dir = os.path.dirname(full_path)

        # Two things matter here so the menu doesn't look "frozen":
        #
        # 1. We minimise the menu window (iconify) before the game opens.
        #    The menu is fullscreen; without this it sits on top and the
        #    game can appear stuck behind it.
        # 2. We run the game with cwd=game_dir. Each game loads its own
        #    images/sounds using relative paths, so it must run *from its
        #    own folder* or it can't find them and hangs on a black screen.
        pygame.display.iconify()

        process = subprocess.Popen([sys.executable, full_path], cwd=game_dir)

        # While the game runs we can't just call .wait() and go silent:
        # the OS would mark the menu window "not responding". Instead we
        # loop, pumping the menu's events every 100 ms so it stays alive,
        # until the game process exits.
        while process.poll() is None:
            pygame.event.pump()
            pygame.time.wait(100)

        if background_music is not None:
            background_music.play(-1)

        # Bring the fullscreen menu back after the game closes.
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    except FileNotFoundError as error:
        logging.error("Could not launch %s: %s", relative_path, error)


def draw_arrows(mouse_pos, page, total_pages):
    """Draw the page arrows and return the two Button objects.

    We return the buttons themselves (or None when an arrow shouldn't
    show) instead of guessing "was it clicked?" here. The caller then
    tests them against the ACTUAL click position inside its event loop.

    This was the bug before: this function decided "clicked" from where
    the mouse was *hovering*, not from a real click, so the page would
    flip at the wrong time — or not at all. Detecting the click where the
    click event actually happens fixes it.
    """
    left_arrow = None
    right_arrow = None

    # Show the left arrow only if there's a previous page.
    if page > 0:
        left_arrow = Button(None, (50, SCREEN_HEIGHT // 2), "<",
                            get_font(50), "White", "Green")
        left_arrow.changeColor(mouse_pos)
        left_arrow.update(SCREEN)

    # Show the right arrow only if there's a next page.
    if page < total_pages - 1:
        right_arrow = Button(None, (SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2), ">",
                             get_font(50), "White", "Green")
        right_arrow.changeColor(mouse_pos)
        right_arrow.update(SCREEN)

    return left_arrow, right_arrow


def programs_screen():
    """Show the paginated list of games and launch the one you click."""
    page = 0
    total_pages = (len(GAMES) + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE

    back_button = Button(None, (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 50),
                        "BACK", get_font(50), "White", "Green")

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        # Figure out which slice of GAMES belongs on this page.
        start = page * GAMES_PER_PAGE
        visible = GAMES[start:start + GAMES_PER_PAGE]

        # Build the buttons for this frame and remember them, so that when a
        # click happens (in the event loop below) we can test each one.
        buttons = []
        for i, game in enumerate(visible):
            button = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + i * 100),
                           game["name"], get_font(30), "Yellow", "Green")
            button.changeColor(mouse_pos)
            button.update(SCREEN)
            buttons.append((button, game))

        left_arrow, right_arrow = draw_arrows(mouse_pos, page, total_pages)
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)

        # Show "Page 1 / 2" and a hint that the arrow keys work.
        if total_pages > 1:
            info = get_font(20).render(
                f"Page {page + 1} / {total_pages}   -   < > or arrow keys",
                True, "White")
            SCREEN.blit(info, info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)))

        # We handle clicks here, inside the event loop, using MOUSEBUTTONDOWN.
        # We test every button against event.pos — the exact spot that was
        # clicked — so one click means exactly one action.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard: LEFT / RIGHT arrows flip pages, ESC goes back.
            # This is the same page change as clicking the on-screen arrows,
            # just more convenient. We clamp with max()/min() so you can't
            # move past the first or last page.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and page > 0:
                    play_click()
                    page -= 1
                    break
                if event.key == pygame.K_RIGHT and page < total_pages - 1:
                    play_click()
                    page += 1
                    break
                if event.key == pygame.K_ESCAPE:
                    play_click()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.checkForInput(event.pos):
                    play_click()
                    return

                if left_arrow is not None and left_arrow.checkForInput(event.pos):
                    play_click()
                    page -= 1
                    break  # page changed: stop testing old buttons this frame

                if right_arrow is not None and right_arrow.checkForInput(event.pos):
                    play_click()
                    page += 1
                    break

                for button, game in buttons:
                    if button.checkForInput(event.pos):
                        play_click()
                        launch_game(game["path"])
                        break

        pygame.display.update()


def show_explanation(text):
    """Draw a panel with the how-to-play text for one game."""
    lines = text.strip().split("\n")
    font = get_font(20)

    back_button = Button(None,
                        (int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.9)),
                        "BACK", get_font(20), "White", "Green")

    while True:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Draw each line of text under the previous one.
        y = SCREEN_HEIGHT // 6
        for line in lines:
            surface = font.render(line, True, "White")
            SCREEN.blit(surface, (SCREEN_WIDTH // 8, y))
            y += surface.get_height() + 5

        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.checkForInput(event.pos):
                    play_click()
                    return

        pygame.display.update()


def guide_screen():
    """Show the paginated list of games; clicking one shows its guide."""
    page = 0
    total_pages = (len(GAMES) + GAMES_PER_PAGE - 1) // GAMES_PER_PAGE

    back_button = Button(None, (SCREEN_WIDTH - 125, SCREEN_HEIGHT - 50),
                        "BACK", get_font(50), "White", "Green")

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        title = get_font(45).render("GUIDE — choose a game", True, "White")
        SCREEN.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)))

        start = page * GAMES_PER_PAGE
        visible = GAMES[start:start + GAMES_PER_PAGE]

        buttons = []
        for i, game in enumerate(visible):
            button = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 60),
                           game["name"], get_font(30), "Yellow", "Green")
            button.changeColor(mouse_pos)
            button.update(SCREEN)
            buttons.append((button, game))

        left_arrow, right_arrow = draw_arrows(mouse_pos, page, total_pages)
        back_button.changeColor(mouse_pos)
        back_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard page navigation, same as on the PROGRAMS screen.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and page > 0:
                    play_click()
                    page -= 1
                    break
                if event.key == pygame.K_RIGHT and page < total_pages - 1:
                    play_click()
                    page += 1
                    break
                if event.key == pygame.K_ESCAPE:
                    play_click()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.checkForInput(event.pos):
                    play_click()
                    return

                if left_arrow is not None and left_arrow.checkForInput(event.pos):
                    play_click()
                    page -= 1
                    break

                if right_arrow is not None and right_arrow.checkForInput(event.pos):
                    play_click()
                    page += 1
                    break

                for button, game in buttons:
                    if button.checkForInput(event.pos):
                        play_click()
                        # Each game now shows its OWN explanation. The old
                        # code accidentally showed the Snake guide for Space
                        # Shooter and Aeroblaster (a copy-paste mistake).
                        show_explanation(game["explanation"])

        pygame.display.update()


def main_menu():
    """The first screen: PROGRAMS, GUIDE, QUIT."""
    menu_buttons = [
        {"name": "PROGRAMS", "action": programs_screen},
        {"name": "GUIDE", "action": guide_screen},
        {"name": "QUIT", "action": None},  # None means "exit the program".
    ]

    while True:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        title = get_font(100).render("MAIN MENU", True, "#b68f40")
        SCREEN.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)))

        buttons = []
        for i, item in enumerate(menu_buttons):
            button = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 150),
                           item["name"], get_font(75), "#d7fcd4", "Green")
            button.changeColor(mouse_pos)
            button.update(SCREEN)
            buttons.append((button, item))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button, item in buttons:
                    if button.checkForInput(event.pos):
                        play_click()
                        if item["action"] is None:
                            pygame.quit()
                            sys.exit()
                        item["action"]()

        pygame.display.update()


# This guard means main_menu() only runs when you execute THIS file
# directly (python main.py), not when another file imports it.
if __name__ == "__main__":
    main_menu()
