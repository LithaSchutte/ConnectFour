"""
File: AI.py
Author: Litha Schutte
Description: AI module for Connect Four.
Implements an AI player using the minimax algorithm for optimal move selection.
Date: 05/2024
"""

from Board import Board
import math
import random


class AI(object):

    def __init__(self, token):
        self.token = token
        self.ai_messages = [  # Courtesy of ChatGPT
            "Analyzing the board for the optimal move...",
            "Evaluating potential strategies...",
            "Considering all possible outcomes...",
            "Calculating the best move...",
            "Anticipating your next move...",
            "Examining the game state...",
            "Formulating a winning strategy...",
            "Searching for the most favourable position...",
            "Preparing to make a decisive move...",
            "Adapting my strategy to counter your moves...",
            "Assessing the board for tactical opportunities...",
            "Focusing on maximizing my chances of winning...",
            "Deploying advanced algorithms to determine the next move...",
            "Strategising to achieve victory...",
            "Thinking several steps ahead to outmaneuver you..."
        ]

    """
    The implementation of the minimax function and the helper functions - evaluate_window, and score_position follow 
    similar logic from https://roboticsproject.readthedocs.io/en/latest/ConnectFourAlgorithm.html with adjustments 
    and improvements.
    """

    def minimax(self, board, depth, alpha, beta, maximizing_player, player_a, player_b):
        valid_locations = board.get_possible_moves()
        is_terminal = board.game_over()

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.evaluate() == player_b.token:
                    return None, 100000000000000
                elif board.evaluate() == player_a.token:
                    return None, -10000000000000
                else:
                    return None, 0
            else:
                return None, score_position(board.board, player_b.token)

        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = [row[:] for row in board.board]
                board.move(col, player_b.token)
                new_score = self.minimax(board, depth - 1, alpha, beta, False, player_a, player_b)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                board.board = [row[:] for row in b_copy]
            return column, value
        else:
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = [row[:] for row in board.board]
                board.move(col, player_a.token)
                new_score = self.minimax(board, depth - 1, alpha, beta, True, player_a, player_b)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
                board.board = [row[:] for row in b_copy]
            return column, value


def score_position(board, token):  # mirror algorithm to evaluate in the Board class
    score = 0
    # Score centre column
    centre_count = sum(1 for i in board[Board.COLUMNS // 2] if i == token)
    score += centre_count * 3
    # Score horizontal, vertical, and diagonal positions
    for r in range(Board.ROWS):
        for c in range(Board.COLUMNS):
            if board[r][c] != " ":
                value = board[r][c]
                # Score horizontal
                if c <= Board.COLUMNS - 4:
                    if all(board[r][c + i] == value for i in range(4)):
                        score += 100 if value == token else -100
                # Score vertical
                if r <= Board.ROWS - 4:
                    if all(board[r + i][c] == value for i in range(4)):
                        score += 100 if value == token else -100
                # Score diagonal (up)
                if c <= Board.COLUMNS - 4 and r >= 3:
                    if all(board[r - i][c + i] == value for i in range(4)):
                        score += 100 if value == token else -100
                # Score diagonal (down)
                if c <= Board.COLUMNS - 4 and r <= Board.ROWS - 4:
                    if all(board[r + i][c + i] == value for i in range(4)):
                        score += 100 if value == token else -100
    return score


def evaluate_window(window, token, player_a, player_b):
    score = 0
    opp_token = player_b.token if token == player_a.token else player_a.token
    token_count = window.count(token)
    opp_token_count = window.count(opp_token)
    empty_count = window.count(" ")
    if token_count == 4:
        score += 100
    elif token_count == 3 and empty_count == 1:
        score += 5
    elif token_count == 2 and empty_count == 2:
        score += 2
    if opp_token_count == 3 and empty_count == 1:
        score -= 4
    return score
