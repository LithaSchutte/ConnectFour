"""
File: Game.py
Author: Litha Schutte
Description: Game module for playing Connect Four on the terminal.
Implements the game logic for Connect Four, including setting up players, handling different game modes,
making moves, and managing game state. Offers options for human vs. human, human vs. random bot,
and human vs. AI gameplay.
Date: 05/2024
"""

import sys
import random
import math
from Board import Board
from Player import Player
from AI import AI


class Game(object):
    def __init__(self):
        # initialise variables
        self.playerA, self.playerB = None, None
        self.turn, self.mode, self.result = 0, None, None
        self.board = Board()

    def setup(self):
        # draw welcome screen
        pattern = "+" + "-" * 28 + "+"
        print(pattern)
        print('| Welcome to ConnectFour!    |')
        print(pattern)
        print('| Please select a game mode: |')
        print('| 1: Human opponent          |')
        print('| 2: Random opponent         |')
        print('| 3: AI opponent             |')
        print(pattern)

        # select game mode
        while True:
            mode = input("Enter your choice (1, 2, or 3): | [R]estart | [Q]uit | : ")
            if mode in ['1', '2', '3']:
                self.mode = mode
                break
            else:
                self.check_restart_or_quit(mode)
                print("Invalid input. Please enter 1, 2, or 3.")
        self.board.create_board()

    # check if the game needs to restart or quit
    def check_restart_or_quit(self, key):
        if key.upper() == "R":  # also allow lowercase input
            self.restart()
        if key.upper() == "Q":  # also allow lowercase input
            self.quit()

    def human_mode(self):  # two humans playing against each other

        self.setup_players(None)

        self.board.print_board()  # initial board

        while not self.result:
            if self.turn == 0:
                player = self.playerA
            if self.turn == 1:
                player = self.playerB
            self.make_move(player)

    def computer_mode(self, opponent):
        self.setup_players(opponent)
        self.board.print_board()

        while not self.result:
            if self.turn == 0:  # Human player's turn
                self.make_move(self.playerA)

            if self.turn == 1:  # Computer's turn
                if self.mode == '2':  # Random bot opponent
                    while True:
                        col = random.randint(0, Board.COLUMNS - 1)  # Generate a random move
                        if col in self.board.get_possible_moves():
                            break
                if self.mode == '3':  # AI Opponent
                    ai = AI(self.playerB.token)
                    col = ai.minimax(self.board, 4, -math.inf, math.inf, True, self.playerA, self.playerB)[0]
                    message = random.choice(ai.ai_messages)
                    print(f"AI Bot: {message}")
                self.board.move(col, self.playerB.token)
                self.end_move()   # check for winner and change turn

    def setup_players(self, opponent):
        self.playerA = Player(input("Enter your username: "))
        self.playerA.token = self.playerA.choose_token()
        print(f'You chose {self.playerA.token}')

        if self.mode == '1':  # Human vs Human
            self.playerB = Player(input("Enter Player B's username: "))
            while self.playerB.name == self.playerA.name:  # Check that players have different usernames
                print('Choose a different username, Player B cannot have the same name as Player A')
                self.playerB = Player(input("Enter Player B's username: "))
            self.playerB.token = self.playerB.choose_token()
            print(f'You chose {self.playerB.token}')

        elif self.mode == '2' or self.mode == '3':
            self.playerB = Player(opponent)
            if self.playerA.token != "X":
                self.playerB.token = "X"
            else:
                self.playerB.token = "O"

    def make_move(self, player):  # human player move
        while True:
            try:
                col = input(f"{player.name}: Enter a column from 1 - {Board.COLUMNS} to drop your token  | [R]estart | [Q]uit | : ")
                self.check_restart_or_quit(col)
                if col.isdigit() and 1 <= int(col) <= Board.COLUMNS:
                    col = int(col)
                    if col - 1 in self.board.get_possible_moves():
                        break
                    else:
                        print("Selected column is full. Please choose another column.")
                else:
                    print("Please enter a valid number between 1 and 7.")
            except ValueError:
                self.check_restart_or_quit(col)
                print("Please enter a valid number.")

        print(f'You dropped a token in column {col}')
        self.board.move(col - 1, player.token)
        self.end_move()

    def end_move(self):  # to be executed after every move -  check for winner and change turn
        self.board.print_board()  # show last move
        self.result = self.board.evaluate()  # check for win or draw condition
        if not self.result:
            self.turn = 1 - self.turn  # Change turn

    def play(self):
        # opponent implementation: Strategy design pattern
        if self.mode == '1':
            self.human_mode()  # human opponent
        elif self.mode == '2':
            self.computer_mode("Random Bot")  # random bot opponent
        elif self.mode == '3':
            self.computer_mode("AI Bot")  # AI opponent

        if self.result:
            if self.result == 'Draw':
                print("The game is a draw.")
            elif self.mode == '1':
                print("Player", self.playerA.name if self.result == self.playerA.token else self.playerB.name, "wins.")
            else:
                print("You won! Congratulations!" if self.result == self.playerA.token else "Unfortunately, the bot won.")

            key = ""
            while key != "R" and key != "Q":
                key = input("Do you want to play again? | [R]estart | [Q]uit | : ").upper()
            self.check_restart_or_quit(key)

    def quit(self):
        confirm = input("Are you sure you want to quit? (yes/no): ").lower()
        if confirm == "yes":
            print("Thanks for playing! Goodbye!")
            sys.exit()
        else:
            print("Resuming game...")

    def restart(self):
        confirm = input("Are you sure you want to restart the game? (yes/no): ").lower()
        if confirm == "yes":
            print("Restarting the game...")
            self.start()
        else:
            print("Resuming game...")

    def start(self):
        try:
            self.result = None
            self.setup()
            self.play()
        except Exception as e:
            print(f"An error occurred: {str(e)}. Exiting game...")  # comment out while debugging
            sys.exit()
