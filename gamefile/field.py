from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('pngfile//field.png')

    def draw(self):
        self.image.draw(800,100,1600,200)

    def update(self):
        pass
class Background:
    def __init__(self):
        self.image = load_image('pngfile//background.png')

    def draw(self):
        self.image.draw(800, 380)

    def update(self):
        pass
class GoalPost:
    def __init__(self, x, y,state):
        self.image = load_image('pngfile//goalpost.png')
        self.x = x
        self.y = y
        self.state = state
    def draw(self):
        if self.state == 0:
            self.image.draw(self.x,self.y, 100, 140)
        if self.state == 1:
            self.image.composite_draw(270.2,'h',self.x,self.y,100,140)

    def update(self):
        pass