'''
Dennis Smith
CS 5001, Spring 2022
Final Project("Mastermind")
Test Mastermind Game

This file is used to test non-Turtle methods and functions within the
Mastermind program.
'''
import unittest
from Gameplay import Gameplay
from Point import Point
from Icon import Icon
from mastermind_codes import *
import pathlib as pl
import os


class TestGameplay(unittest.TestCase):
    '''
    Test class for the Gameplay and Icon class and their methods
    '''
    def test_load_past_scores_error(self):
        # Cleaning up to make sure no old files
        if os.path.exists(LEADERBOARD):
          os.remove(LEADERBOARD)
        else:
          print("The file does not exist")
        with self.assertRaises(Exception):
            Gameplay.load_past_scores(self)

    def test_load_past_scores(self):
        # Cleaning up to make sure no old files
        if os.path.exists(ERROR_FILE):
          os.remove(ERROR_FILE)
        else:
          print("The file does not exist")
        with open(LEADERBOARD, 'w+') as file:
            file.write("x, 18")
        Gameplay.load_past_scores(self)
        self.assertFalse(os.path.isfile(ERROR_FILE))

    def test_log_error(self):
        exception_text = "this is a test exception"
        found = False
        Gameplay.log_error(self,Exception(exception_text))
        with open(ERROR_FILE, 'r+') as file:
            if(exception_text in file.read()):
                found = True
        self.assertTrue(found)

    def test_create_code(self):
        result = create_code()
        self.assertTrue(len(result)==4)
        self.assertTrue(type(result) == list)

    def test_compare_code_guess_partial(self):
        input1 = ['green', 'black', 'blue', 'purple']
        input2 = ['green', 'yellow', 'blue', 'purple']
        result = compare_code_guess(input1, input2)
        self.assertTrue(result == (3,0))

    def test_compare_code_guess_full_match(self):
        input1 = ['green', 'black', 'blue', 'purple']
        input2 = ['green', 'black', 'blue', 'purple']
        result = compare_code_guess(input1, input2)
        self.assertTrue(result == (4,0))
        
    def test_compare_code_guess_no_match(self):
        input1 = ['green', 'black', 'blue', 'purple']
        input2 = ['purple', 'blue', 'yellow', 'green']
        result = compare_code_guess(input1, input2)
        self.assertTrue(result == (0,3))
    
    def test_compare_code_guess_error(self):
        input1 = ['green', 'black', 'blue', 'purple']
        input2 = ['hello', 'fake']
        with self.assertRaises(Exception):
            compare_code_guess(input1, input2)

    def test_icon_clicked(self):
        icon = Icon(Point(5,5),10,10,WINPIC)
        self.assertTrue(icon.clicked_in_region(6,8))

    def test_icon_clicked_false(self):
        icon = Icon(Point(5,5),10,10,WINPIC)
        self.assertFalse(icon.clicked_in_region(100,8))

def main():
    unittest.main(verbosity = 3)

if __name__ == "__main__":
    main()



    
