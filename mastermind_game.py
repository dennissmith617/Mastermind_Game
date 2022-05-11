'''
Dennis Smith
CS 5001, Spring 2022
Final Project("Mastermind")
Mastermind Game

This file houses the main function for the Mastermind game. It is supported
mainly by the Gameplay class, which calls some other classes and functions
to run the program. In this program, the Gameplay class is initiated, the
user's name is entered, the borders on the screen are drawn, and interactive
marbles and icons are placed on the screen. The game then handles user clicks
on the screen as the game itself is played.
'''

from Gameplay import *

screen = turtle.Screen()

def main():
    gameplay = Gameplay(Point(0, 0), "red")
    # Get user
    gameplay.init_user()
    # Draw Game Area
    gameplay.draw_border(-270, -200, 300, 490)
    # Draw Interaction Area
    gameplay.draw_border( -270, -285, 530, 75)
    # Draw Leaderboard Area
    gameplay.draw_border(50, -200, 210, 490, "blue")
    # Initiate gameplay elements
    gameplay.init_sel_marble()
    gameplay.init_icons()
    gameplay.init_feedback_circles()
    # Handle clicks and actual gameplay
    screen.onclick(gameplay.click_marbles)

if __name__ == "__main__":
    main()
