"""
File: Main.py
Author: Litha Schutte
Description: This Python script implements a simple game loop. It starts the game by creating an instance of
the 'Game' class which allows players to play Connect Four on the Python terminal. Players can play the game
repeatedly until they choose to quit.
Date: 05/2024.
   _____                            _     ______
  / ____|                          | |   |  ____|
 | |     ___  _ __  _ __   ___  ___| |_  | |__ ___  _   _ _ __
 | |    / _ \| '_ \| '_ \ / _ \/ __| __| |  __/ _ \| | | | '__|
 | |___| (_) | | | | | | |  __/ (__| |_  | | | (_) | |_| | |
  \_____\___/|_| |_|_| |_|\___|\___|\__| |_|  \___/ \__,_|_|

"""

from Game import Game


def main():
    while True:
        game = Game()
        game.start()

        restart_or_quit = input("Do you want to play again? (Y/N): ").upper()
        if restart_or_quit != 'Y':
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()
