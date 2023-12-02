import random

from pico2d import *


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
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(400) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(800) - self.ch // 2, self.h - self.ch - 1)
class GoalPost:
    def __init__(self, x, y,state):
        self.image = load_image('pngfile//goalpost.png')
        self.x = x
        self.y = y
        self.point_1p = 0
        self.point_2p = 0
        self.state = state
        self.font = load_font('ENCR10B.TTF', 32)
    def draw(self):
        if self.state == 0:
            self.image.draw(self.x,self.y, 100, 140)
            self.font.draw(self.x+850, self.y +400, f'{self.point_2p:01d}', (255, 255, 255))
            draw_rectangle(*self.get_bb())
        if self.state == 1:
            self.image.composite_draw(270.2,'h',self.x,self.y,100,140)
            self.font.draw(self.x-850, self.y +400, f'{self.point_1p:01d}', (255, 255, 255))
            draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 30, self.y - 80, self.x+30,self.y+500
    def handle_collision(self,group,other):
        if group == 'ball:post_a':
            if other.y <= 200:
                self.point_2p += 1
                other.x = 500
                other.y = 300
                other.bounce_rate = 1
                other.x_velocity,other.y_velocity = 4, 4
                other.launch_angle = -90
            else:
                other.x_velocity *=-1
        if group == 'ball:post_b':
            if other.y <= 200:
                other.x = 1100
                other.y = 300
                other.bounce_rate = 1
                other.x_velocity,other.y_velocity = 4, 4
                other.launch_angle = -90
                self.point_1p += 1
            else:
                other.x_velocity *=-1
        pass
    def update(self):
        pass