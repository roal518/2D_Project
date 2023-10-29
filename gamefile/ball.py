from pico2d import load_image


class Idle:
    pass
class Run:
#    @staticmethod
    pass
class Sleep:
    pass



class Ball:
    def __init__(self, x = 400, y = 300, velocity = 1):
        self.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        self.y += self.velocity
