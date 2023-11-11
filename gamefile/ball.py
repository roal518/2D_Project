import random

from pico2d import *
import game_world
import game_framework
import math
GROUND = 65
CEILING = 600
LEFT_WALL = 10
RIGHT_WALL = 1600-10
class Run:
    pass
class Move:
    pass
class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.x_velocity, self.y_velocity = x, y, velocity , velocity
        self.launch_angle = 90
        self.bounce_rate = 1
    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
    def update(self):
        self.x += (self.x_velocity * 200
                   * game_framework.frame_time
                   * math.cos(math.radians(self.launch_angle)))
        self.y += (self.y_velocity * 200
                   * game_framework.frame_time
                   * math.sin(math.radians(self.launch_angle)))
        self.x = clamp(LEFT_WALL, self.x, RIGHT_WALL)
        if self.x <= LEFT_WALL:
            self.x_velocity /= -1
        elif self.x >= RIGHT_WALL:
            self.x_velocity *= -1
        self.y = clamp(GROUND,self.y,CEILING)
        if self.y <= GROUND:
            self.y_velocity /= -1
            self.bounce_rate += 1
        elif self.y >= CEILING/self.bounce_rate:
            self.y_velocity *= -1


    # fill here
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x+10,self.y+10

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.launch_angle = random.randint(0,90)
            self.bounce_rate = 1
            self.velocity = random.randint(1,5)
            pass
# 공이 닿으면 player의 중심점과 공의 중심점이 연결되는
# 선분과 x축이 만드는 각도를 구해서 launch_angle을 바꿔준다.
#