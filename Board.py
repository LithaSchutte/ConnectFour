"""
File: Board.py
Author: Litha Schutte
Description: Board module for representing the game board in Connect Four.
Implements a board class with methods for creating the board, making moves, printing the board,
evaluating game state for a win or draw, and providing helper functions for AI move selection.
Date: 05/2024
"""


class Board(object):

    # constant board size - scalable
    ROWS = 6
    COLUMNS = 7

    def __init__(self):  # constructor
        self.board = None
        self.moveCount = 0
        self.winner = None

    def create_board(self):  # create 2D array to store the board
        self.board = []
        for i in range(self.ROWS):  # rows
            self.board.append([' '] * self.COLUMNS)  # columns
        return self.board

    def move(self, column, piece):
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][column] == " ":
                self.board[row][column] = piece
                self.moveCount += 1  # Increment move count to eventually find a drawn position
                return
        print("Invalid Move: Column is full")

    def print_board(self):  # draws the board on the terminal
        for col in range(1, self.COLUMNS + 1):  # number columns at the top
            print(f"   {col}  ", end="")
        print()
        for row in range(self.ROWS):
            print("-" * (self.ROWS * self.COLUMNS + 1))
            print("| ", end=" ")
            for col in range(self.COLUMNS):
                print(self.board[row][col], " | ", end=" ")
            print()
        print("-" * (self.ROWS * self.COLUMNS + 1))
        for col in range(1, self.COLUMNS + 1):  # number columns at the bottom
            print(f"   {col}  ", end="")
        print()

    def evaluate(self):
        if self.moveCount == self.ROWS * self.COLUMNS:
            return 'Draw'

        for col in range(self.COLUMNS):
            for row in range(self.ROWS):
                if self.board[row][col] != " ":
                    piece = self.board[row][col]

                    # Check horizontal
                    if col <= self.COLUMNS - 4:
                        if all(self.board[row][col + i] == piece for i in range(4)):
                            self.winner = piece
                            return self.winner

                    # Check vertical
                    if row <= self.ROWS - 4:
                        if all(self.board[row + i][col] == piece for i in range(4)):
                            self.winner = piece
                            return self.winner

                    # Check diagonal (up)
                    if col <= self.COLUMNS - 4 and row >= 3:
                        if all(self.board[row - i][col + i] == piece for i in range(4)):
                            self.winner = piece
                            return self.winner

                    # Check diagonal (down)
                    if col <= self.COLUMNS - 4 and row <= self.ROWS - 4:
                        if all(self.board[row + i][col + i] == piece for i in range(4)):
                            self.winner = piece
                            return self.winner
        return None

    # Helper functions for Minimax
    def get_possible_moves(self):  # get possible moves for AI
        possible_moves = []
        for col in range(self.COLUMNS):
            for row in range(self.ROWS - 1, -1, -1):
                if self.board[row][col] == ' ':
                    possible_moves.append(col)
                    break  # Break after finding the topmost empty row in the column
        return possible_moves

    def game_over(self):  # Check for game over
        if self.evaluate():
            return True
        return False
