'''
Dennis Smith
CS 5001, Spring 2022
Final Project("Mastermind")
Gameplay

This file houses the Gameplay class, which is the bulk of the Mastermind
program. Gameplay is initiated here by drawing borders, the leaderboard,
interactive feedback and selection marbles, pegs (bulls and cows), and then
handling clicks to keep track of the user's progress through the game.
Leaderboard files and error files are also handled, and the user's name is
taken so that they may be added to the leaderboard.
'''
import turtle
import time

from datetime import datetime
from Icon import *
from Marble import *
from mastermind_constants import *
from mastermind_codes import *
from turtle import Screen, Turtle
import os

screen = turtle.Screen()

class Gameplay:
    '''
    Gameplay handles the initialization of the Mastermind game, as well as the
    scoring, maintenance, and points-and-clicks necessary to handle user
    interaction. This class will take the user's name, run the game, and log
    their score via the leaderboard file. Errors related to running the game
    are handled as well.
    '''
    def __init__(self, position, color, size = MARBLE_RADIUS):
        '''
        Method -- __init__
            Initializes the Gameplay class. Declares settings mainly for
            turtle usage, lists for tracking marble and peg coordinates,
            active playing rows, and the user's score. Finally, gets the
            game's secret code via the create_code function.

        Parameters:
            position(Point(x,y)) -- Coordinates developed via the Point class
            color(str) -- Marble or peg color
            size(int) -- Radius size for the marble or peg

        Returns nothing
        '''
        self.pen = self.new_pen()
        self.user = ''
        self.color = color
        self.position = position
        self.pen.hideturtle()
        self.size = size
        self.pen.speed("fastest")

        self.starting_position = Point(EMP_MARB_X,EMP_MARB_Y)
        self.input_marble_start = Point(SEL_MARB_START_X, SEL_MARB_START_Y)
 
        self.feedback_circles = []
        self.feedback_pegs = []
        self.marble_row = []
        self.icon_lst = []
        self.score_lst = []

        self.playing_row = 0
        self.curr_score = 1
        
        self.color_code = create_code()

    def new_pen(self):
        '''
        Method -- new_pen
            Returns a turtle instance to the user when called.

        Returns a turtle
        '''
        return turtle.Turtle()
    
    def init_user(self):
        '''
        Method -- init_user
            Initializes the leaderboard, and prompts the user to input their
            username before playing.

        Returns nothing
        '''
        welcome = "Welcome to Mastermind!"
        ask_name = "Please enter your name: "
        self.user = turtle.textinput(welcome, ask_name)
        self.init_leaderboard()

    def draw_marble(self, color='white', size=MARBLE_RADIUS):
        '''
        Method -- draw_marble
            Draws a marble (or circle) based on the color and radius provided

        Parameters:
            color(str) -- Marble or peg color
            size(int) -- Radius size for the marble or peg

        Returns nothing
        '''
        self.pen.up()
        self.pen.goto(self.position.x, self.position.y)
        self.pen.down()
        self.pen.fillcolor(color)
        self.pen.begin_fill()
        self.pen.circle(size)
        self.pen.end_fill()

    def init_leaderboard(self):
        '''
        Method -- __init_leaderboard
            Initializes the leaderboard by opening the leaderboard file,
            sorting the scores by lowest to highest, and writing the ranked
            scores in the leaderboard on the game screen.

        Parameters:
            None

        Returns nothing
        '''
        # List of ordered, loaded scores from file
        self.score_lst = self.order_scores(self.load_past_scores())
        #Write header
        self.init_leader_header()
        
        self.pen.penup()
        self.pen.goto(LEADERBOARD_USE_X, LEADERBOARD_USE_Y)
        self.pen.pendown()
        
        full_string = ''
        new_y = LEADERBOARD_USE_Y
        # 18 score entries is the limit for the on screen leaderboard
        if len(self.score_lst) > 18:
            self.score_lst = self.score_lst[:18]
    
        for i in range(len(self.score_lst)):
            user = self.score_lst[i][0]
            score = self.score_lst[i][1]
            fmt = "{} : {}".format(user, score)
            self.pen.write(fmt, font=("Monaco", 14, "normal"), align = "left")
            self.pen.penup()
            new_y -= 25
            self.pen.goto(LEADERBOARD_USE_X, new_y)
            self.pen.pendown()
            
    def load_past_scores(self):
        '''
        Method -- load_past_scores
            Opens the named leaderboard file and returns a list of the lines
            within the file. If the file cannot be found, an error is logged
            and a new file is written.

        Parameters:
            None

        Returns lines, a list of the lines within the opened file. If no file
            is present, lines is returned as an empty list.
        '''
        # Opens leaderboard file housing scores
        try:
            with open(LEADERBOARD, 'r+') as file:
                lines = file.readlines()
                
        except Exception as argument:
            self.error_icon(LDR_ERROR_PIC)
            self.log_error(argument)
            with open(LEADERBOARD, 'w+') as file:
                lines = []

        return lines

    def log_error(self, argument):
        '''
        Method -- log_error
            Logs an error passed from either opening the leaderboard file or
            accessing the program's images. Provides the date and time of
            the error, as well as the error itself (passed in as argument).

        Parameters:
            argument(str) - the specific error thrown in one of the
            try/except scenarios.

        Returns nothing
        '''
        if os.path.exists(ERROR_FILE):
            with open(ERROR_FILE, "a") as file:
                err_string = '{}:ERROR: {}\n'.format(datetime.now(), argument)
                file.write(err_string)
                
        else:
            with open(ERROR_FILE, "w+") as file:
                err_string = '{}:ERROR: {}\n'.format(datetime.now(), argument)
                file.write(err_string)
    
    def order_scores(self, past_scores):
        '''
        Method -- order_scores
            Reorders the scores from the opened leaderboard file from
            lowest to highest. This makes the initialization of the
            leaderboard more efficient and shows proper ranking.

        Parameters:
            position(Point(x,y)) -- A list of the past scores which have been
            opened and placed into a list in the
            "load_past_scores" method.

        Returns self.score_lst, an instance variable which has ordered the
            leaderboard scores from lowest (best) to highest score.
        '''
        sub_score_lst = []
        for result in past_scores:
            if result.strip() != "":
                user, score = result.strip().split(',')
                sub_score_lst = [user, int(score)]
                self.score_lst.append(sub_score_lst)
        self.score_lst.sort(key = lambda x:x[1])

        return self.score_lst

    def init_leader_header(self):
        '''
        Method -- init_leader_header
            Draws the header for the leaderboard above the user scores.

        Parameters:
            None

        Returns nothing
        '''
        self.pen.penup()
        self.pen.goto(LEADERBOARD_HEAD_X, LEADERBOARD_HEAD_Y)
        self.pen.pendown()
        self.pen.write("Leaderboard", font = ("Monaco",24, "normal"), align = "center")
        
    def add_new_score(self):
        '''
        Method -- add_new_score
            Adds the user's score to the leaderboard file. If the file is
            below the 18 user-score threshold, their name and score are
            simply added. If it is a new user and the file is at its
            threshold, the highest (worst) score in the file is deleted.
                
        Parameters:
            None

        Returns nothing
        '''
        user_entry = [self.user, self.curr_score]
        with open(LEADERBOARD, 'w+') as file:
            
            if len(self.score_lst) < 18:
                self.score_lst.append(user_entry)
            elif len(self.score_lst) >= 18:
                self.score_lst = self.score_lst[:-1]
                self.score_lst.append(user_entry)
                
            for i in range(len(self.score_lst)):
                name = self.score_lst[i][0]
                score = self.score_lst[i][1]
                entry_string = '{},{}\n'.format(name,score)
                file.write(entry_string)
        

    def draw_border(self, x, y, width, length, color = "black"):
        '''
        Method -- draw_border
            Draws borders on the screen based on starting position, width,
            length, and border color

        Parameters:
            x(int) -- Starting x coordinate for the border
            y(int) -- Starting y coordinate for the border
            width(int) -- horizontal border distance
            length(int) -- vertical border distance
            color(str) -- Color of the border when drawn

        Returns nothing
        '''
        self.pen.width(BORDER_WIDTH)
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pencolor(color)
        self.pen.pendown()
        for i in range(2):
            self.pen.forward(width)
            self.pen.left(BORDER_ANGLE)
            self.pen.forward(length)
            self.pen.left(BORDER_ANGLE)
        self.pen.width(1)

    def init_feedback_circles(self):
        '''
        Method -- init_feedback_circles
            Initializes the drawing and coordinate setting process for the
            10 rows of 4 feedback marbles and the 10 rows of 4 pegs (also
            known as bulls and cows). Loops through all 10 rows while calling
            the methods necessary for drawing the marbles and circles. Also
            resets the position at the end of each row to faciliate proper row
            formatting.
            

        Parameters:
            None

        Returns nothing
        '''
        self.position = self.starting_position
        for i in range(10):
            guess_circles, peg_rows = self.draw_circle_peg()
            # feedback_circles holds coordinate list for drawing later
            self.feedback_circles.append(guess_circles)
            # feedback_pegs holds coordinate list for drawing later
            self.feedback_pegs.append(peg_rows)
            
            # resets coordinates for next row
            self.position.x -= 180
            self.position.y -= 60

    def draw_circle_peg(self):
        '''
        Method -- draw_circle_peg
            Draws a row of 4 empty marbles and creates a list of their
            coordinates. Also calls the draw_guess_pegs method to begin
            drawing pegs at the end of each row.

        Parameters:
            Nothing

        Returns circle_row, guess_pegs. Both are lists which will serve to
            provide coordinates when handling clicks and redrawing with
            new colors.
        '''
        circle_row = []
        for i in range(4):
            marble = Marble(Point(self.position.x, self.position.y))
            circle_row.append(marble)
            marble.draw()
            self.position.x += 40

        guess_pegs = self.draw_guess_pegs()
        for each in circle_row:
            return circle_row, guess_pegs

    def draw_guess_pegs(self):
        '''
        Method -- draw_guess_pegs
            Draws the four guess pegs at the end of each feedback row. Does
            so by drawing the two left marbles before then drawing the two
            right marbles.

        Parameters:
            None

        Returns peg_rows, a list used to provide coordinates when handling
        clicks and redrawing black (correct color and position) or red
        (correct collors, incorrect position) pegs
        '''
        # Draws guess pegs, returning list of rows for coordinate use
        peg_rows = []
        start_x = self.position.x
        start_y = self.position.y
        self.position.y += 15
        col = "white"

        for j in range(2):
            # Draws first 2 guess pegs (left top, left bottom)
            marb = Marble(Point(self.position.x, self.position.y), col, PEG_RAD)
            peg_rows.append(marb)
            marb.draw()
            self.position.y -= 10
            
        self.position.x += 10
        self.position.y += 20
        
        for i in range(2):
            # Draws next two guess pegs
            marb = Marble(Point(self.position.x, self.position.y), col, PEG_RAD)
            peg_rows.append(marb)
            marb.draw()
            self.position.y -= 10

        # Reset back to inital coordinates for next row
        self.position.y += 20
        self.position.x += 10

        return peg_rows

    def init_sel_marble(self):
        '''
        Method -- init_sel_marble
            Initializes the selection marbles for player interaction. Loops
            through the list of provided marble colors: draws the marble
            and sets the position for each color.

        Parameters:
            None

        Returns nothing
        '''
        self.position = self.input_marble_start
        for each in COLORS:
            marble = Marble(Point(self.position.x, self.position.y), color = each)
            self.marble_row.append(marble)
            marble.draw()
            self.position.x += 42

    def init_icons(self):
        '''
        Method -- init_icons
            Initializes the image icons. These are the buttons present on the
            screen during gameplay. These include the check button, x button,
            and quit button. This method calls a method for each of them.

        Parameters:
            None.

        Returns nothing
        '''
        self.check_button()
        self.x_button()
        self.quit_button()
        
    def check_button(self):
        '''
        Method -- check_button
            Places the check button on the screen by returning an
            instance of icon_add for the check button

        Parameters:
            None

        Returns an instance of the icon add method for the check button
        '''
        return self.icon_add(Point(CHECK_BUT_X, CHECK_BUT_Y), CHECK_BUT)
            

    def x_button(self):
        '''
        Method -- x_button
            Places the x button on the screen by returning an
            instance of icon_add for the x button.

        Parameters:
            None

        Returns an instance of the icon_add method for the x button
        '''
        return self.icon_add(Point(X_BUT_X, X_BUT_Y), X_BUT)

    def quit_button(self):
        '''
        Method -- quit_button
            Places the quit button on the screen by returning an
            instance of icon_add for the quit button.

        Parameters:
            None

        Returns an instance of the icon_add method for the quit button
        '''
        return self.icon_add(Point(Q_BUT_X, Q_BUT_Y), QUIT_BUT)

    def icon_add(self, position, icon, width=30, length=30):
        '''
        Method -- icon_add
            Registers and stamps a shape based on user input. This will add
            images to the screen for use either as interactive buttons (check,
            x, quit) or as images (winning pic, losing pic, quit pic, errors).

        Parameters:
            position(Point(x,y)) -- Coordinates developed via the Point class
            icon(str) -- The image being registered and stamped
            width(int) -- Width of the shape that will register clicks (for use
                in the Icon class)
            length(int) -- Length of the shape that will register clicks (for sue
                in the Icon class)

        Returns nothing
        '''
        screen = Screen()
        try:
            screen.register_shape(icon)
        except Exception as argument:
            self.error_icon(FI_ERROR_PIC)
            self.log_error(argument)
            quit()

        turtle = Turtle(shape=icon)
        
        turtle.penup()

        turtle.goto(position.x, position.y)
        turtle.stamp()
        turtle.shape("classic")
        turtle.penup()

        
        icon = Icon(position, width, length, icon)
        self.icon_lst.append(icon)
        turtle.hideturtle()

    def error_icon(self, image):
        '''
        Method -- error_icon
            Registers, stamps, and then clears the error icon on the screen.
            Remains present on the screen for 5 seconds before disappearing.

        Parameters:
            image(str) - a string representing the name of the error image
            to be displayed

        Returns nothing
        '''
        x = 0
        y = 0
        
        screen = Screen()
        screen.register_shape(image)

        turtle = Turtle(shape=image)
        
        turtle.penup()

        turtle.goto(x, y)
        err_pic = turtle.stamp()
        turtle.shape("classic")
        turtle.penup()

        time.sleep(5)
        turtle.clearstamp(err_pic)
        
        turtle.hideturtle()
        
    def click_marbles(self, x, y):
        '''
        Method -- click_marbles
            Handles user clicks from the interactive marble section. If
            the marble in this section is "white", it has already been
            used and will be ignored. Else, it begin looking at the
            playing_row (or active feedback marble row). If the marble
            in this row is "white", it will set that marble as the
            new position before drawing a colored marble (based on the
            players selected color) over that position. It will then
            redraw the interactive marble color chosen by the user as
            "white" to prevent them from choosing that color again during
            their current turn. Also creates an instance of click_icons
            to check for user clicks on the icons.

        Parameters:
            x(int) -- x coordinate of click
            y(int) -- y coordinate of  click

        Returns nothing
        '''
        for marb in self.marble_row:
            if marb.clicked_in_region(x, y):
                # No action if clicked marble in interactive row is white
                if marb.color == "white":
                    break
                #playing_row is list of specific feedback row (starts at 0)
                playing_row = self.feedback_circles[self.playing_row]
                #Loop through 4 marbles in playing_row
                for i in range(len(playing_row)):
                    if playing_row[i].color == "white":
                        self.position.x = playing_row[i].position.x
                        self.position.y = playing_row[i].position.y
                        # Redraw white feedback marble with chosen color
                        self.draw_marble(marb.color)
                        self.feedback_circles[self.playing_row][i].color = marb.color
                        self.position.x = marb.position.x
                        self.position.y = marb.position.y
                        marb.color = "white"
                        # Redraw selected interactive marble as white
                        self.draw_marble()
                        break
                    else:
                        continue

        # Check how many marbles filled out, only want to submit if all 4            
        marbleCount = 0
        for each in self.feedback_circles[self.playing_row]:
            if each.color != 'white':
                marbleCount = marbleCount + 1
      
        self.click_icons(marbleCount, x,y)

    def click_icons(self, marbleCount, x,y):
        '''
        Method -- click_icons
            Handles user clicks for the on-screen icons (check, x, quit). If
            the clicked_in_region method registers clicking within an icon,
            this method runs an instance of a method built specifically to
            handle clicks for that icon
            
        Parameters:
            marbleCount -- number of marbles clicked
            x(int) -- x coordinate of click
            y(int) -- y coordinate of  click

        Returns nothing
        '''
        for icon in self.icon_lst:
            if icon.clicked_in_region(x, y):
                if icon.icon == CHECK_BUT and marbleCount == 4:
                    self.check_guess()
                elif icon.icon == X_BUT:
                    self.reset_marbles_curr_row()
                elif icon.icon == QUIT_BUT:
                    self.finish_game()
    
    def check_guess(self):
        '''
        Method -- check_guess
            Compares the user's guesses within the active playing row to
            the color_code instance holding the secret code. The function
            compare_code_guess returns the number of black and red pegs,
            which are then drawn on teh screen using a for loop for the black
            peg and a for loop for the red peg. If there are 4 black pegs or
            the playing row count exceeds the 10 rows, the game ends. Else,
            the playing row is increased by 1, the current score is set to the
            playing row count, and the interaction marbles are reset so the
            player may make another attempt.

        Parameters:
            None

        Returns nothing
        '''
        guess = [marb.color for marb in self.feedback_circles[self.playing_row]]
        blk_peg, rd_peg = compare_code_guess(self.color_code, guess)

        if blk_peg > 0 or rd_peg > 0:
            row_count = 0
            # Fill out the black pegs
            for each in range(blk_peg):
                curr_marb_row = self.feedback_pegs[self.playing_row]
                curr_marb = curr_marb_row[row_count]
                self.position.x = curr_marb.position.x
                self.position.y = curr_marb.position.y
                self.draw_marble("black", PEG_RAD)
                row_count += 1
            # Fill out the red pegs
            for each in range(rd_peg):
                curr_marb_row = self.feedback_pegs[self.playing_row]
                curr_marb = curr_marb_row[row_count]
                self.position.x = curr_marb.position.x
                self.position.y = curr_marb.position.y
                self.draw_marble("red", PEG_RAD)
                row_count += 1

                
        
        if blk_peg == 4 or self.playing_row >= 9:
            self.finish_game(blk_peg)

        self.playing_row += 1
        self.curr_score += 1
        self.reset_sel_marble()

    def reset_sel_marble(self):
        '''
        Method -- reset_sel_marble
            Resets the interactive selection marbles so that the user regains
            full access to marble color choice. Does this by looking through
            the marble row and resetting any "white" marble color with its
            corresponding color in the COLORS list.

        Parameters:
            None

        Returns nothing
        '''
        for i in range(len(self.marble_row)):
            if self.marble_row[i].color == "white":
                self.marble_row[i].color = COLORS[i]
                self.set_position(self.marble_row[i].position.x, self.marble_row[i].position.y)
                self.draw_marble(COLORS[i])

    def set_position(self, x, y):
        '''
        Method -- __init__
            Sets the position for resetting selection marbles or resetting
            the current row of feedback marbles. Sets the position based on
            positions developed for the feedback and interactive marble rows.

        Parameters:
            x(int) -- x coordinate based on given position
            y(int) -- y coordinate based on give nposition

        Returns nothing
        '''
        self.position.x = x
        self.position.y = y

    def finish_game(self, blk_peg = 0):
        '''
        Method -- finish_game
            Checks to see if the user has won, lost, or quit the game based on
            peg count or score. If 4 black pegs are passed to the method via
            check_guess, the player has won. A new score will be written and
            the winner picture will appear before the game ends. If the score
            is 10, the player has lost the game by running out of guesses. In
            this scenario, the score will be added and a losing picture will
            appear. Finally, the player may hit the quit button, which will
            bring up the quit picture.

        Parameters:
            blk_peg(int) -- the number of black pegs based on the user's guess,
            which is passed from the check_guess method.

        Returns nothing
        '''
        if blk_peg == 4:
            self.add_new_score()
            self.icon_add(Point(0,0), WINPIC, 300, 300)
            time.sleep(5)
            quit()
            
        elif self.curr_score == 10:
            self.add_new_score()
            self.icon_add(Point(0,0), LOSEPIC, 300, 300)
            time.sleep(5)
            quit()
            
        else:
            self.icon_add(Point(0,0), QUITPIC, 300, 300)
            time.sleep(5)
            quit()
            
    def reset_marbles_curr_row(self):
        '''
        Method -- reset_marbles_curr_row
            Initiates the reset process should the user click the check button.
            This will reset the interactive marble row, as well as the current
            feedback row.

        Parameters:
            None

        Returns nothing
        '''
        self.reset_sel_marble()
        self.reset_curr_row()

    def reset_curr_row(self):
        '''
        Method -- reset_curr_row
            Resets the feedback circles in the current feedback row to be
            blank, should the user choose to redo their guess.

        Parameters:
            None

        Returns nothing
        '''
        for marb in self.feedback_circles[self.playing_row]:
            if marb.color != "white":
                marb.color = "white"
                self.set_position(marb.position.x, marb.position.y)
                self.draw_marble(marb.color)
            
