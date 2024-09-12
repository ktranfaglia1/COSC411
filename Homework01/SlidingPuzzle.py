import sys
import random
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

CELL_COUNT = 4
CELL_SIZE = 125
GRID_ORIGINX = 150
GRID_ORIGINY = 150
W_WIDTH = 800
W_HEIGHT = 800

class SlidingPuzzle(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('SlidingPuzzle')
        self.setGeometry(300, 300, W_WIDTH, W_HEIGHT)
        self.__moves = 0
        self.__complete = False
        self.__solvable = False
        self.__board = [[-1 for _ in range(CELL_COUNT)] for _ in range(CELL_COUNT)]
        self.initialize_board()
        self.show()

    def initialize_board(self):
        self.__order = list(range(CELL_COUNT * CELL_COUNT))  # Shuffle the order array
        random.shuffle(self.__order)

        # Populate the board with the shuffled numbers
        index = 0
        for r in range(CELL_COUNT):
            for c in range(CELL_COUNT):
                self.__board[r][c] = self.__order[index]
                index += 1

    def paintEvent(self, event):
        qp = QPainter()
        blackPen = QPen(QBrush(Qt.black), 1)
        qp.begin(self)

        qp.fillRect(event.rect(), Qt.white)
        qp.setPen(blackPen)

        font = QFont('Arial', 20)
        qp.setFont(font)

        for r in range(len(self.__board)):
            for c in range(len(self.__board[r])):
                # Draw the cell border
                qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                # Get the number at the current position
                number = self.__board[r][c]

                # Only draw the number if it's not 0 (0 represents the empty tile)
                if number != 0:
                    text = str(number)
                    
                    # Calculate initial text_x to center horizontally
                    text_x = GRID_ORIGINX + c * CELL_SIZE + CELL_SIZE // 2 - 10
                    
                    # Adjust text_x for double-digit numbers
                    if len(text) == 2:
                        text_x -= 10  # Shift text to the left for double digits; adjust value as needed

                    text_y = GRID_ORIGINY + r * CELL_SIZE + CELL_SIZE // 2 + 10  # Center vertically

                    qp.drawText(text_x, text_y, text)

        qp.end()

    def mousePressEvent(self, event):
        # Get the exact x and y coordinates of the click
        x = event.x()
        y = event.y()

        # Print the click coordinates
        print(f"Click coordinates: x={x}, y={y}")

        row = (event.y() - GRID_ORIGINY) // CELL_SIZE
        col = (event.x() - GRID_ORIGINX) // CELL_SIZE

        if 0 <= row < CELL_COUNT and 0 <= col < CELL_COUNT:
            print(row, col)
            if self.__board[row][col] != -1:
                self.__board[row][col] = 0
            print(self.__board)
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SlidingPuzzle()
    sys.exit(app.exec_())
