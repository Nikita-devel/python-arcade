import numpy as np  # Importation du module numpy pour manipuler des tableaux multidimensionnels

class Board:
    def __init__(self, row_count, column_count):
        # Set up the Board with the given number of rows and columns
        self.row_count = row_count  # Nombre de lignes dans le tableau
        self.column_count = column_count  # Nombre de colonnes dans le tableau
        self.grid = np.zeros((row_count, column_count))  # Create a grid of zeros to represent the game board

    def is_valid_location(self, column):
        # Check whether the top row in the column is empty
        return self.grid[self.row_count - 1, column] == 0

    def get_next_open_row(self, column):
        # Return the first row that is empty
        for row in range(self.row_count):
            if self.grid[row, column] == 0:
                return row

    def drop_piece(self, row, column, turn):
        # Fill the given spot with the current player
        self.grid[row, column] = turn

    def has_four_in_a_row(self, turn):
        # Check horizontally
        for r in range(self.row_count):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r, c + 1] == turn and self.grid[r, c + 2] == turn and self.grid[r, c + 3] == turn:
                    return True

        # Check vertically
        for r in range(self.row_count - 3):
            for c in range(self.column_count):
                if self.grid[r, c] == turn and self.grid[r + 1, c] == turn and self.grid[r + 2, c] == turn and self.grid[r + 3, c] == turn:
                    return True

        # Check the upward diagonal
        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r + 1, c + 1] == turn and self.grid[r + 2, c + 2] == turn and self.grid[r + 3, c + 3] == turn:
                    return True

        # Check the downward diagonal
        for r in range(3, self.row_count):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r - 1, c + 1] == turn and self.grid[r - 2, c + 2] == turn and self.grid[r - 3, c + 3] == turn:
                    return True

        return False

    def get_winning_cells(self, turn):
        # Like has_four_in_a_row, but returns the LIST of the 4 winning
        # cells (r, c) so we can highlight them on screen.
        # Returns an empty list if there is no winner.
        lines = []
        # Horizontal
        for r in range(self.row_count):
            for c in range(self.column_count - 3):
                lines.append([(r, c + i) for i in range(4)])
        # Vertical
        for r in range(self.row_count - 3):
            for c in range(self.column_count):
                lines.append([(r + i, c) for i in range(4)])
        # Upward diagonal
        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                lines.append([(r + i, c + i) for i in range(4)])
        # Downward diagonal
        for r in range(3, self.row_count):
            for c in range(self.column_count - 3):
                lines.append([(r - i, c + i) for i in range(4)])

        for cells in lines:
            if all(self.grid[r, c] == turn for r, c in cells):
                return cells
        return []

    def is_full(self):
        # Check whether every cell in the grid is filled
        return self.grid.all()

    def reset(self):
        # Fill the grid with zeros for a new round
        self.grid = np.zeros((self.row_count, self.column_count))

    def print_grid(self):
        # Print the game state to the console
        print(np.flip(self.grid, 0))  # Utilisation de np.flip pour inverser l'ordre des lignes et rendre l'affichage plus intuitif