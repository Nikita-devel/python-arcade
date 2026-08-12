"""
Connect 4 (Puissance 4) — two players on one keyboard/mouse.

What changed and WHY:
  * The old version used tkinter pop-up dialogs for the "you win / play
    again?" question. Mixing tkinter with pygame made the whole window
    freeze when someone won. Everything is now drawn with pygame, so the
    game never hands control to a second GUI library. No more freeze.
  * The graphics were flat rectangles and circles. They now have a
    gradient board, soft shadows on the pieces, a hover preview of where
    your piece will drop, and the four winning pieces flash to celebrate.

Controls:
  * Move the mouse to choose a column, left-click to drop.
  * After a game ends: press ENTER to play again, ESC to quit.
"""

import sys
import math

import pygame

import board  # local file: the game logic (grid, win checks)

# --- Colors (R, G, B) ------------------------------------------------------
# Named colors make the drawing code below easy to read.
BLACK = (10, 10, 15)
BOARD_BLUE = (33, 79, 198)
BOARD_BLUE_DARK = (20, 52, 140)
EMPTY_HOLE = (18, 18, 28)
RED = (222, 60, 65)
RED_DARK = (150, 30, 35)
YELLOW = (245, 205, 60)
YELLOW_DARK = (170, 135, 20)
WHITE = (240, 240, 245)


def lerp_color(color_a, color_b, t):
    """Blend two colors. t=0 gives color_a, t=1 gives color_b.

    Used to paint a smooth vertical gradient on the board.
    """
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))


class Pane:
    """Everything about DRAWING the board lives here.

    The game rules live in board.Board; this class only turns that state
    into pixels.
    """

    def __init__(self, row_count, column_count, square_size):
        self.board = board.Board(row_count, column_count)
        self.square_size = square_size
        self.radius = square_size // 2 - 6
        self.width = column_count * square_size
        # One extra row at the top is the "on deck" area where your next
        # piece hovers before you drop it.
        self.height = (row_count + 1) * square_size
        self.row_offset = square_size
        self.circle_offset = square_size // 2
        self.screen = pygame.display.set_mode((self.width, self.height))

    def _piece_center(self, r, c):
        """Return the pixel (x, y) center of the hole at grid row r, col c.

        Row 0 is the bottom of the board, so we flip it vertically.
        """
        x = c * self.square_size + self.circle_offset
        y = self.height - (r * self.square_size + self.circle_offset)
        return x, y

    def draw_piece(self, x, y, base, dark):
        """Draw one glossy disc with a shadow, a rim, and a highlight."""
        # Drop shadow, slightly offset down-right.
        shadow = pygame.Surface((self.radius * 2 + 6, self.radius * 2 + 6),
                                pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 90),
                           (self.radius + 3, self.radius + 5), self.radius)
        self.screen.blit(shadow, (x - self.radius - 3, y - self.radius - 3))
        # Darker rim, then the main color on top = a simple 3D look.
        pygame.draw.circle(self.screen, dark, (x, y), self.radius)
        pygame.draw.circle(self.screen, base, (x, y), self.radius - 3)
        # Small light spot in the upper-left for a shiny highlight.
        hx, hy = x - self.radius // 3, y - self.radius // 3
        pygame.draw.circle(self.screen, lerp_color(base, WHITE, 0.45),
                           (hx, hy), max(3, self.radius // 4))

    def draw_background(self, hover_x=None, hover_turn=None):
        """Repaint the whole board for one frame.

        hover_x / hover_turn draw the translucent preview piece that
        follows the mouse across the top row.
        """
        self.screen.fill(BLACK)

        # Preview piece in the top "on deck" strip.
        if hover_x is not None and hover_turn is not None:
            col = min(max(hover_x // self.square_size, 0),
                      self.board.column_count - 1)
            preview_x = col * self.square_size + self.circle_offset
            base = RED if hover_turn == 1 else YELLOW
            ghost = pygame.Surface((self.radius * 2, self.radius * 2),
                                   pygame.SRCALPHA)
            pygame.draw.circle(ghost, (*base, 120),
                               (self.radius, self.radius), self.radius)
            self.screen.blit(ghost, (preview_x - self.radius,
                                     self.circle_offset - self.radius))

        # The blue board with round holes punched out of it.
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                left = c * self.square_size
                top = r * self.square_size + self.row_offset
                # Vertical gradient: lighter at top, darker at bottom.
                t = r / max(1, self.board.row_count - 1)
                cell_color = lerp_color(BOARD_BLUE, BOARD_BLUE_DARK, t)
                pygame.draw.rect(self.screen, cell_color,
                                 (left, top, self.square_size, self.square_size))
                cx = left + self.circle_offset
                cy = top + self.circle_offset
                # The hole: dark disc with a subtle inner shadow ring.
                pygame.draw.circle(self.screen, EMPTY_HOLE, (cx, cy), self.radius)
                pygame.draw.circle(self.screen, BOARD_BLUE_DARK, (cx, cy),
                                   self.radius, 2)

        self.fill_in_pieces(update=False)
        pygame.display.update()

    def fill_in_pieces(self, update=True):
        """Draw every dropped piece currently on the board."""
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                value = self.board.grid[r, c]
                if value == 0:
                    continue
                x, y = self._piece_center(r, c)
                if value == 1:
                    self.draw_piece(x, y, RED, RED_DARK)
                else:
                    self.draw_piece(x, y, YELLOW, YELLOW_DARK)
        if update:
            pygame.display.update()

    def try_drop_piece(self, x_position, turn):
        """Drop a piece in the column under x_position, if that column has room."""
        column_selection = x_position // self.square_size
        if 0 <= column_selection < self.board.column_count \
                and self.board.is_valid_location(column_selection):
            row = self.board.get_next_open_row(column_selection)
            self.board.drop_piece(row, column_selection, turn)
            return True
        return False

    def flash_winning_cells(self, cells):
        """Make the four winning pieces pulse a few times to celebrate."""
        clock = pygame.time.Clock()
        for frame in range(60):
            # A sine wave gives a smooth 0..1..0 brightness pulse.
            glow = (math.sin(frame * 0.3) + 1) / 2
            self.draw_background()
            for (r, c) in cells:
                x, y = self._piece_center(r, c)
                ring = pygame.Surface((self.radius * 2 + 12, self.radius * 2 + 12),
                                      pygame.SRCALPHA)
                alpha = int(120 + glow * 135)
                pygame.draw.circle(ring, (255, 255, 255, alpha),
                                   (self.radius + 6, self.radius + 6),
                                   self.radius + 4, 5)
                self.screen.blit(ring, (x - self.radius - 6, y - self.radius - 6))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)

    def show_game_over(self, winner):
        """Draw the end-of-game banner IN pygame (no tkinter = no freeze).

        Returns True if the player wants to play again, False to quit.
        Waits for ENTER (replay) or ESC / window close (quit).
        """
        # Dim the board behind a translucent overlay.
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        big_font = pygame.font.SysFont("arialrounded", 48, bold=True)
        small_font = pygame.font.SysFont("arial", 24)

        if winner:
            color = RED if winner == 1 else YELLOW
            title = big_font.render(f"Player {winner} wins!", True, color)
        else:
            title = big_font.render("It's a draw!", True, WHITE)
        hint = small_font.render("ENTER = play again     ESC = quit", True, WHITE)

        self.screen.blit(title, title.get_rect(
            center=(self.width // 2, self.height // 2 - 20)))
        self.screen.blit(hint, hint.get_rect(
            center=(self.width // 2, self.height // 2 + 40)))
        pygame.display.update()

        # Block here until the player decides, but keep the event loop
        # alive so the window never looks frozen.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        return False
            pygame.time.wait(20)

    def reset(self):
        """Clear the board for a new game."""
        self.board.reset()
        self.draw_background()


def main():
    pygame.init()
    pygame.display.set_caption("Connect 4")
    pane = Pane(6, 7, 90)

    turn = 1
    hover_x = pane.width // 2
    pane.draw_background(hover_x, turn)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                hover_x = event.pos[0]

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pane.try_drop_piece(event.pos[0], turn):
                    winning = pane.board.get_winning_cells(turn)
                    if winning:
                        pane.flash_winning_cells(winning)
                        if pane.show_game_over(turn):
                            pane.reset()
                            turn = 1
                        else:
                            running = False
                    elif pane.board.is_full():
                        if pane.show_game_over(None):
                            pane.reset()
                            turn = 1
                        else:
                            running = False
                    else:
                        # Switch player.
                        turn = 2 if turn == 1 else 1

        # Redraw once per frame with the current hover preview.
        pane.draw_background(hover_x, turn)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
