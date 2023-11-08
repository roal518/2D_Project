
from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('field.png')

    def draw(self):
        self.image.draw(400, 100,1600,200)

    def update(self):
        pass
class Background:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        self.image.draw(600, 380)

    def update(self):
        pass
class GoalPost:
    def __init__(self):
        self.image = load_image('goalpost.png')

    def draw(self):
        self.image.draw(0,120,100,150)

    def update(self):
        pass