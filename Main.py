"""
File: Main.py
Author: Litha Schutte
Description: This Python script implements a simple game loop. It starts the game by creating an instance of
the 'Game' class which allows players to play Connect Four on the Python terminal. Players can play the game
repeatedly until they choose to quit.
Date: 05/2024.
"""

from Game import Game

def main():
    while True:
        game = Game()
        game.start()


if __name__ == "__main__":
    main()
