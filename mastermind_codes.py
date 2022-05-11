'''
Dennis Smith
CS 5001, Spring 2022
Final Project("Mastermind")
Mastermind Codes

This program houses the functions that create and check against the Mastermind
secret code.
'''
from mastermind_constants import *
import random

def create_code(colors = COLORS):
    '''
    Function -- create_code

        Takes the COLORS list and develops a secret code of 4 colors for
        use in the Mastermind game

    Parameters:

        colors (list) - List of colors from the COLORS constant
        
    Returns color_code, the secret code used to play Mastermind.
    '''
    color_code = []
    i = 1
    
    while i < 5:
        marble_col = random.choice(COLORS)
        if marble_col in color_code:
            pass
        else:
            color_code.append(marble_col)
            i += 1
    return color_code

def compare_code_guess(color_code, player_guess):
    '''
    Function -- compare_code_guess

        Takes the color developed in create_code and compares with
        the player's guess (via the Gameplay method). Returns the number
        of black and red pegs based on the user's guess.

    Parameters:

        color_code (list) - List of colors from the COLORS constant
        player_guess (list) - List of colors from the player's guess
        
    Returns blk_peg, rd_peg. blk_peg is correct color and position.
    rd_peg is correct color, but wrong position.Both are integers that
    represent the number of pegs of each color based on the user's guess.
    '''
    if len(color_code) != 4 or len(player_guess) != 4:
        # Check that the lists are both 4 to prevent error.
        raise Exception("Code & Player Guess should each have length 4")
    
    play_guess = player_guess
    blk_peg = 0
    rd_peg = 0
    
    for i in range(len(color_code)):
        if color_code[i] == play_guess[i]:
            blk_peg += 1
        elif play_guess[i] in color_code and color_code[i] != play_guess[i]:
            rd_peg += 1
        else:
            pass

    return (blk_peg, rd_peg)
