Dennis Smith
Mastermind Program

This program runs a single player version of the code-breaking game Mastermind. Player's have 10
opportunities to guess a secret code consisting of 4 colored marbles. Their guesses are evaluated using pegs, where black pegs denote the correct color in the correct place, and red pegs denote the correct color in the wrong place. The player's score is determined by the number of guesses they have to make to uncover the correct code. For this game, the lowest score wins. If the player cannot guess the correct code in 10 guesses, they have lost.

I used this project to showcase the knowledge gained in my Fundamentals of Computer Science Course. The majority of the game is run through the Gameplay class, where I have used a variety of methods to initialize the game board, execute the game, and record scores or log errors. Coordinates for drawn elements are handled via multiple lists, which help when iterating through guess attempts. Finally, all active gameplay is handled via click methods related to the interactive guessing marbles or the buttons available onscreen.