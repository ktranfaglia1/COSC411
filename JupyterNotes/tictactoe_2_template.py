import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

# if you change CELL_COUNT, be sure that initial
# patterns in constructor are still valid
CELL_COUNT = 3
CELL_SIZE = 50
GRID_ORIGINX = 175
GRID_ORIGINY = 175
W_WIDTH = 500
W_HEIGHT = 500

class TicTacToe(QWidget):

  def __init__(self):
    super().__init__()
    self.setWindowTitle('TicTacToe')
    self.setGeometry(300, 300, W_WIDTH,W_HEIGHT)
    self.__turn = 0
    self.__winner = False
    self.__board = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
    self.show()


  def paintEvent(self, event):
    qp = QPainter()

    blackPen = QPen(QBrush(Qt.black), 1)

    qp.begin(self)

    # Clear the background
    qp.fillRect(event.rect(), Qt.white)

    qp.setPen(blackPen) 

    for r in range(len(self.__board)):
      for c in range(len(self.__board[r])):
        qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if (self.__is_winning_square(r,c) is True):
          qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        if (self.__board[r][c] == 0):
          qp.drawLine(GRID_ORIGINX + c * CELL_SIZE + 3, GRID_ORIGINY + r * CELL_SIZE + 3, GRID_ORIGINX + c * CELL_SIZE \
                      + CELL_SIZE - 3, GRID_ORIGINY + r * CELL_SIZE + CELL_SIZE - 3)
          qp.drawLine(GRID_ORIGINX + c * CELL_SIZE + CELL_SIZE - 3, GRID_ORIGINY + r * CELL_SIZE + 3, GRID_ORIGINX + c * \
                      CELL_SIZE + 3, GRID_ORIGINY + r * CELL_SIZE + CELL_SIZE - 3)
        elif (self.__board[r][c] == 1):
          qp.drawEllipse(GRID_ORIGINX + c * CELL_SIZE + 3, GRID_ORIGINY + r * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE -6)
        qp.setPen(Qt.black)

    qp.end()

  def mousePressEvent(self, event):
    if (self.__winner is True):
      return
    row = (event.y() - GRID_ORIGINY) // CELL_SIZE
    col = (event.x() - GRID_ORIGINX) // CELL_SIZE

    if (0 <= row < CELL_COUNT and 0 <= col < CELL_COUNT):
      print(row, col)
      if (self.__board[row][col] == -1):
        self.__board[row][col] = self.__turn
        self.__turn = (self.__turn + 1) % 2
      print(self.__board)
    self.update()

  def __is_winning_square(self, r, c):
    for i in range(CELL_COUNT):
      # Row winner
      if (self.__board[i][0] != -1 and (self.__board[i][0] == self.__board[i][1] and self.__board[i][1] == self.__board[i][2])):
        self.__winner = True
        return r == i
      # Column winner
      if (self.__board[0][i] != -1 and (self.__board[0][i] == self.__board[1][i] and self.__board[1][i] == self.__board[2][i])):
        self.__winner = True
        return c == i
      # First diagonal winner
      if (self.__board[0][0] != -1 and (self.__board[0][0] == self.__board[1][1]) and self.__board[1][1] == self.__board[2][2]):
        self.__winner = True
        return r == c
      # Second diagonal winner
      if (self.__board[0][2] != -1 and (self.__board[0][2] == self.__board[1][1]) and self.__board[1][1] == self.__board[2][0]):
        self.__winner = True
        return (r + c == 2)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = TicTacToe()
  sys.exit(app.exec_())
