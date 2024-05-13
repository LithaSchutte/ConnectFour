"""
File: Player.py
Author: Litha Schutte
Description: Player module for representing players in Connect Four.
Implements a player class with a name and token attributes. Allows players to choose their token
(symbol) for the game.
Note: Could be directly incorporated into the Game class but is kept separate to allow possible future extension
Date: 05/2024
"""


class Player(object):

    def __init__(self, name):
        self.token = None
        self.name = name

    def choose_token(self):
        from Game import Game  # to avoid circular import
        game = Game()

        while True:
            try:
                token = (input(f"{self.name}: Choose a symbol to represent your token, e.g X or O | "
                               f"[R]estart | [Q]uit | "))
                game.check_restart_or_quit(token)
                if len(token) != 1:
                    raise ValueError("Please enter only one character.")
                else:
                    break
            except ValueError as e:
                print(e)
        return token
