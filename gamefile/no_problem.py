from pico2d import *

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = load_image('animation_sheet.png')