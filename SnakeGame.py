#Extra Credit - I. No direction reversal
import random, tkinter as tk

#==========================================
# Purpose: The object of this class represents the snake game. This object controls different elements of the game.
# Instance variables: 
# win - represents the window in which the game will take place 
# canvas - represents the canvas in the window on which the game elements will be displayed
# board - represents the area in which the player snake is allowed to move. If the player snake goes outside this area the game ends.
# player - object of the snake class. This snake is controlled by the user.
# enemy - object of the enemy class. This snake is controlled by the computer.
# message - this stores the id of the text box which is displayed at the end of the game
# food_x - stores the x coordinate of the upper left corner of the food pellet (integer)
# food_y - stores the y coordinate of the upper left corner of the food pellet (integer)
# food - stores the id of the food pellet displayed on the canvas
# Methods:
# __init__ - Initialises the instance variables, binds the keys and starts the game
# bind_keys - binds the Up, DOwn, Left, Right and r keys
# new_game - clears the board, resets all the instance variables and starts a new game
# gameloop - keeps the game running till the player snake does not lose
#==========================================

class SnakeGUI:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Snake Game')
        self.canvas = tk.Canvas(self.win, width = 660, height = 660)
        self.canvas.pack()
        self.board = self.canvas.create_rectangle(30, 30, 630, 630)
        self.player = Snake(330, 330, "green", self.canvas)
        self.enemy = Snake(30, 30, "purple", self.canvas)
        self.message = ''
        self.food_x = 30*random.randint(1,20)
        self.food_y = 30*random.randint(1,20)
        self.food = self.canvas.create_oval(self.food_x , self.food_y, self.food_x + 30, self.food_y + 30, fill="red")
        self.bind_keys()
        self.gameloop()
    def new_game(self, event):
        if not self.player.get_alive():
            for ele in self.player.get_segments():
                 self.canvas.delete(ele)
            for ele in self.enemy.get_segments():
                self.canvas.delete(ele)
            self.canvas.delete(self.food)
            self.canvas.delete(self.message)
            self.player = Snake(330, 330, "green", self.canvas)
            self.enemy = Snake(30, 30, "purple", self.canvas)
            self.food_x = 30*random.randint(1,20)
            self.food_y = 30*random.randint(1,20)
            self.food = self.canvas.create_oval(self.food_x , self.food_y, self.food_x + 30, self.food_y + 30, fill="red")
            self.bind_keys()
            self.gameloop()
    def bind_keys(self):
        self.win.bind('<Down>',self.player.go_down)
        self.win.bind('<Up>',self.player.go_up)
        self.win.bind('<Right>',self.player.go_right)
        self.win.bind('<Left>',self.player.go_left)
        self.win.bind('r',self.new_game)
        
    def gameloop(self):
        if self.player.get_alive():
            if self.player.player_move(self.food_x, self.food_y, self.enemy.get_segments()) or self.enemy.enemy_move(self.food_x, self.food_y, self.player.get_segments()):
                self.canvas.delete(self.food)
                self.food_x = 30*random.randint(1,20)
                self.food_y = 30*random.randint(1,20)
                self.food = self.canvas.create_oval(self.food_x , self.food_y, self.food_x + 30, self.food_y + 30, fill="red")
            if self.enemy.game_over(self.player.get_segments()):
                self.player.set_alive(False)
            self.canvas.after(250, self.gameloop)
        else:
            self.message = self.canvas.create_text(310, 330, text='Game Over. Score = '+str(len(self.player.segments)))

#==========================================
# Purpose: An object of this class represents a snake (player or enemy)
# Instance variables: 
# x - the x coodinate of the upper left corner of the head of the snake (integer)
# y - the y coodinate of the upper left corner of the head of the snake (integer)
# color - stores a string representing the color of the snake
# canvas - stores the canvas object on which the snake is displayed
# segments - a list of ids of the segments of the snake
# vx - velocity of the snake in the x direction (integer)
# vy - velocity of the snake in the y direction (integer)
# alive - boolean value which is True till the conditions which require the game to be over are not fulfilled
# Methods:
# __init__ - initialises the instance variable and puts the first segment of the snake on the board
# player_move - moves the player snake by one block (30 x 30 pixels). Checks three of the conditions which require
# the game to be over and if they are fulfilled then the alive instance variable is set to False. Checks if the snake
# has eaten the food pellet and returns a boolean value accordingly
# game_over - checks if the snake's head overlaps with one of the segments in the list passed as an argument to this
# function. Returns True if the conditions for the game to be over are fulfilled
# enemy_move - moves the enemy snake by one block (30 x 30 pixels). Checks if the snake
# has eaten the food pellet and returns a boolean value accordingly
# get_segments - returns the list of ids of the segments of the snake
# get_alive - returns the value of the variable alive
# set_alive - sets alive to the value passed as an argument to this function
# go_down - changes the direction of the snake to downwards 
# go_up - changes the direction of the snake to upwards 
# go_right - changes the direction of the snake to the right
# go_left - changes the direction of the snake to the left
#==========================================

class Snake:
    def __init__(self, x, y, color, canvas_obj):
        self.x = x
        self.y = y
        self.color = color
        self.canvas = canvas_obj
        self.segments = []
        self.segments.append(self.canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill=self.color))
        self.vx = 30
        self.vy = 0
        self.alive = True
        
    def player_move(self, food_x, food_y, enemy_segments):
        self.x+=self.vx
        self.y+=self.vy
        self.segments.insert(0, self.canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill=self.color))
        if self.game_over(self.segments[1:]) or self.game_over(enemy_segments):
            self.alive = False
            return False
        elif self.x in [0,630] or self.y in [0,630]:
            self.alive = False
            self.canvas.delete(self.segments.pop())
            return False
        elif self.x == food_x and self.y == food_y:
            return True
        else:
            self.canvas.delete(self.segments.pop())
            return False
    def game_over(self, other_segments):
        for ele in other_segments:
            ls = self.canvas.coords(ele)
            if ls[0]==self.x and ls[1]==self.y:
                self.canvas.delete(self.segments.pop())
                return True
        return False
        
    def enemy_move(self, food_x, food_y, player_segments):
        self.vx = 0
        self.vy = 0
        if self.x > food_x:
            self.vx = -30
        elif self.x < food_x:
            self.vx = 30
        elif self.y > food_y:
            self.vy = -30
        else:
            self.vy = 30
        self.x+=self.vx
        self.y+=self.vy
        self.segments.insert(0, self.canvas.create_rectangle(self.x, self.y, self.x+30, self.y+30, fill=self.color))
        if self.x == food_x and self.y == food_y:
            return True
        else:
            self.canvas.delete(self.segments.pop())
            return False
    def get_segments(self):
        return self.segments
    def get_alive(self):
        return self.alive
    def set_alive(self, value):
        self.alive = value
    def go_down(self,event):
        if self.vy==0:
            self.vx = 0
            self.vy = 30
    def go_up(self,event):
        if self.vy==0:
            self.vx = 0
            self.vy = -30
    def go_right(self,event):
        if self.vx==0:
            self.vx = 30
            self.vy = 0
    def go_left(self,event):
        if self.vx==0:
            self.vx = -30
            self.vy = 0
            
SnakeGUI()
tk.mainloop()

