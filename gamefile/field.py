import time
from pico2d import *
import game_framework
import server
import end_1P
import end_2P
import title_mode
class CountdownTimer:
    def __init__(self, minutes, seconds):
        self.duration = minutes * 60 + seconds
        self.start_time = None
        self.end_time = None
    def start(self):
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration
    def time_left(self):
        if self.start_time is not None and self.end_time is not None:
            return max(0, self.end_time - time.time())
        elif self.start_time is not None:
            return max(0, self.duration - (time.time() - self.start_time))
        else:
            print("Error: Timer not started.")
            return None
    def reset(self):
        self.start_time = None
        self.end_time = None

class Grass:
    def __init__(self):
        self.image = load_image('pngfile//background.png')
        self.font = load_font('ENCR10B.TTF', 32)
        self.min = 1
        self.sec = 30
        self.timer = CountdownTimer(minutes= self.min,seconds=self.sec)
        self.timer.start()
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = 600
    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        self.font.draw(480, 550, f'{self.min:01d}'":", (255, 255, 255))
        self.font.draw(520, 550, f'{self.sec:01d}', (255, 255, 255))
    def update(self):
        print(self.timer.time_left())
        self.window_left = clamp(0, int(server.balls.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.balls.y) - self.ch // 2, self.h - self.ch - 1)
        self.min = int(self.timer.time_left() // 60)
        self.sec = int(self.timer.time_left() % 60)
        if self.min == 0 and self.sec == 0:
            if server.goalpost_A.point_1p > server.goalpost_A.point_2p:
               server.goalpost_A.check = 1
            elif server.goalpost_A.point_1p < server.goalpost_A.point_2p:
                server.goalpost_B.check = 2

class GoalPost:
    def __init__(self, x, y,state):
        self.image = load_image('pngfile//goalpost.png')
        self.x = x
        self.y = 100
        self.point_1p = 0
        self.point_2p = 0
        self.check = 0
        self.state = state
        self.font = load_font('ENCR10B.TTF', 32)
    def draw(self):
        if self.state == 0:
            self.image.draw(self.x - server.background.window_left,self.y, 100, 140)
            self.font.draw(600,500, f'{self.point_2p:01d}', (255, 255, 255))
        if self.state == 1:
            self.image.composite_draw(0,'h',self.x - server.background.window_left,self.y,100,140)
            self.font.draw(400, 500, f'{self.point_1p:01d}', (255, 255, 255))
        if self.check == 1:
            self.font.draw(450, 300, "Win 1P", (255, 255, 255))
            game_framework.change_mode(end_1P)
        if self.check == 2:
            self.font.draw(450, 300, "Win 2P", (255, 255, 255))
            game_framework.change_mode(end_2P)

    def get_bb(self):
        return self.x - 30, self.y - 80, self.x+25,self.y+500
    def handle_collision(self,group,other):
        if group == 'ball:post_a':
            if other.y <= 160:
                self.point_2p += 1
                other.x = 500
                other.y = 300
                other.bounce_rate = 1
                other.x_velocity,other.y_velocity = 4, 4
                other.launch_angle = -90
            else:
                other.x_velocity *=-1
        if group == 'ball:post_b':
            if other.y <= 140:
                other.x = 1100
                other.y = 300
                other.bounce_rate = 1
                other.x_velocity,other.y_velocity = 4, 4
                other.launch_angle = -90
                self.point_1p += 1
            else:
                other.x_velocity *=-1
    def update(self):
        if self.point_1p >= 10:
            self.check = 1
        elif self.point_2p >= 10:
            self.check = 2
