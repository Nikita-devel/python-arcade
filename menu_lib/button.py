"""
A reusable clickable text button for pygame menus.

Instead of copy-pasting the same "draw text, check if the mouse is over it,
change color on hover" code everywhere, we put it in one class. Every menu
screen creates Button objects and reuses this logic. This is a core idea in
programming: write it once, use it many times.
"""


class Button:
    """A piece of text you can hover over and click.

    Parameters
    ----------
    image : pygame.Surface or None
        An optional background image. If None, the text itself becomes the
        clickable area (which is what this project always does).
    pos : (int, int)
        The (x, y) center of the button on the screen.
    text_input : str
        The words shown on the button, e.g. "PLAY".
    font : pygame.font.Font
        The font used to render the text.
    base_color : str
        The normal text color, e.g. "White" or "#d7fcd4".
    hovering_color : str
        The color shown when the mouse is over the button.
    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        # render() turns a string into a picture (a Surface) we can draw.
        # True means "anti-aliasing on" — it smooths the edges of the letters.
        self.text = self.font.render(self.text_input, True, self.base_color)

        # If no image was given, the text becomes the button's image, so the
        # clickable area is exactly the text.
        if self.image is None:
            self.image = self.text

        # A "rect" is a rectangle describing where something sits on screen.
        # get_rect(center=...) centers the rectangle on our chosen point.
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """Draw the button (and its background image, if any) onto the screen."""
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """Return True if the given (x, y) point is inside the button.

        We compare the point against the four edges of the rectangle. The
        old version used `x in range(left, right)`, which builds a whole
        range object every time just to test one number. A simple
        `left <= x <= right` does the same thing, is faster, and is easier
        to read.
        """
        x, y = position
        inside_x = self.rect.left <= x <= self.rect.right
        inside_y = self.rect.top <= y <= self.rect.bottom
        return inside_x and inside_y

    def changeColor(self, position):
        """Recolor the text: hover color if the mouse is over it, else normal.

        This is why buttons "light up" when you point at them.
        """
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
