import sys
import random
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

# Set game specifications: window size, cell/grid size, cell count, and grid starting location
CELL_COUNT = 4
CELL_SIZE = 150
GRID_ORIGINX = 100
GRID_ORIGINY = 100
W_WIDTH = 800
W_HEIGHT = 800


# Sliding puzzle object to handle all game setup and functionality
class SlidingPuzzle(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SlidingPuzzle')
        self.setGeometry(300, 300, W_WIDTH, W_HEIGHT)
        self.__moves = 0
        self.__complete = False
        self.__board = [[-1 for _ in range(CELL_COUNT)] for _ in range(CELL_COUNT)]
        self.__order = None
        self.initialize_board()
        self.show()

    # Initializes the board with random cell numbers if solvable
    def initialize_board(self):
        # Initialize and shuffle the cell order array
        self.__order = list(range(CELL_COUNT * CELL_COUNT))

        # Shuffle the board order until permutation is solvable
        while (not self.is_solvable()):
            random.shuffle(self.__order)

        # Populate the board with the shuffled numbers by row
        index = 0
        for r in range(CELL_COUNT):
            for c in range(CELL_COUNT):
                self.__board[r][c] = self.__order[index]
                index += 1

    # Check if the current board shuffle is solvable using a mathematical formula that counts inversions
    def is_solvable(self):
        inversions = self.count_inversions()  # Get number of inversions
        empty_row = CELL_COUNT - (self.__order.index(0) // CELL_COUNT)  # Find row from bottom with empty cell

        # Check grid width (compatible with future cell amount changes) and assess inversions rule
        if (CELL_COUNT % 2 == 1):  # Odd Width
            return inversions % 2 == 0
        else:  # Even Width
            if (empty_row % 2 == 1):  # Empty space on an odd row (counting from the bottom)
                return inversions % 2 == 0
            else:  # Empty space on an even row
                return inversions % 2 == 1

    # Count the number of inversions on the board (when a cell precedes another cell with a smaller number on it)
    def count_inversions(self):
        inversions = 0
        # Loop through 1D ordered board and counting inversions (ignore empty cell)
        for i in range(len(self.__order)):
            for j in range(i + 1, len(self.__order)):
                if self.__order[i] != 0 and self.__order[j] != 0 and self.__order[i] > self.__order[j]:
                    inversions += 1
        return inversions

    # Creates and updates game grid
    def paintEvent(self, event):
        # Setup QPainter
        qp = QPainter()
        qp.begin(self)

        # Fill the entire grid region with light grey color
        grid_width = grid_height = CELL_COUNT * CELL_SIZE
        qp.fillRect(GRID_ORIGINX, GRID_ORIGINY, grid_width, grid_height, QColor(200, 200, 200))

        # Set text font and draw the move counter above the top-left corner of the grid
        qp.setFont(QFont('Arial', 15))
        qp.drawText(GRID_ORIGINX, GRID_ORIGINY - 10, f"Moves: {self.__moves}")
        qp.setFont(QFont('Arial', 18))

        # Loop through 2D board array and draw the board with numerically labeled cells
        for r in range(len(self.__board)):
            for c in range(len(self.__board[r])):
                number = self.__board[r][c]  # Get the number at the current position

                # Draw the number if it's not 0 (0 represents the empty tile)
                if (number != 0):
                    # Calculate cell center (x,y)
                    text_x = GRID_ORIGINX + c * CELL_SIZE + CELL_SIZE // 2 - 10  # Center horizontally
                    text_y = GRID_ORIGINY + r * CELL_SIZE + CELL_SIZE // 2 + 10  # Center vertically

                    # Adjust x coordinate to center for double-digit numbers
                    if (number / 10 >= 1):
                        text_x -= 10  # Shift text to the left for double digits

                    qp.drawText(text_x, text_y, str(number))  # Draw the number centered in the cell
                else:
                    # Fill the empty block with a blue color
                    qp.fillRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE,
                                QColor(70, 130, 180))

                # Draw the cell border
                qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        qp.end()

    # Handle mouse click event
    def mousePressEvent(self, event):
        # Get the exact x and y coordinates of the click
        y = event.y()
        x = event.x()

        # Print the click coordinates
        print(f"Click coordinates: x={x}, y={y}")

        # Calculate row and column of mouse click
        row = (y - GRID_ORIGINY) // CELL_SIZE
        col = (x - GRID_ORIGINX) // CELL_SIZE

        # Check that the row and column are within the CELL_COUNT * CELL_COUNT grid
        if (0 <= row < CELL_COUNT and 0 <= col < CELL_COUNT):
            # Find the position of the empty cell (denoted by 0)
            empty_row, empty_col = self.find_empty_cell()

            # Check if the clicked cell is adjacent to the empty cell
            if (self.is_adjacent(row, col, empty_row, empty_col)):
                # Swap the clicked cell with the empty cell using the python single line swap
                self.__board[empty_row][empty_col], self.__board[row][col] = self.__board[row][col], \
                    self.__board[empty_row][empty_col]
                self.__moves += 1
                self.update()

    # Return location (row, column) of the empty cell
    def find_empty_cell(self):
        # Find the row and column of the empty cell (denoted by 0)
        for r in range(CELL_COUNT):
            for c in range(CELL_COUNT):
                if self.__board[r][c] == 0:
                    return r, c

    # Return boolean that indicates if the cells are adjacent (swappable)
    def is_adjacent(self, row, col, empty_row, empty_col):
        # Check if the clicked cell is adjacent to the empty cell
        return (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SlidingPuzzle()
    sys.exit(app.exec_())
