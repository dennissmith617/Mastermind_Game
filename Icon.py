'''
Dennis Smith
CS 5001, Spring 2022
Final Project("Mastermind")

This file houses the Icon class, which is used to initialize and check for
clicks in the region of images used in the Mastermind program.
'''

class Icon:
    '''
    Icon initaites instances of images used for the Mastermind game,
    and registers if users have clicked in the region of the Icons
    present on the board.
    '''
    def __init__(self, position, width, height, icon):
        '''
        Method -- __init__
            Initializes the Icon class. Declares settings mainly for
            registering clicks.

        Parameters:
            position(Point(x,y)) -- Coordinates developed via the Point class
            width(int) -- width of the image for registering clicks
            height(int) -- height of the image for registering clicks
            icon(str) - Name of the gif image being initiated

        Returns nothing
        '''
        self.position = position
        self.width = width
        self.height = height
        self.icon = icon

    def clicked_in_region(self, x, y):
        '''
        Method -- clicked_in_region
            Returns a boolean value if the user has clicked in the region
            of an icon instance. This is taken from the Marble class.

        Parameters:
            x -- x coordinate of the image position
            y -- y coordinate of the image position

        Returns nothing
        '''
        if abs(x - self.position.x) <= self.width * 2 and \
           abs(y - self.position.y) <= self.height * 2:
            return True
        return False 
