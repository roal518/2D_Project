# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *
from ball import Ball
import random
import math
import game_framework
import play_single_mode
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
# state event check`
# ( state event type, event value )
# time_out = lambda e : e[0] == 'TIME_OUT'
CEILING = 300
FLOOR = 110

# Boy Run Speed
PIXEL_PER_METER = (20.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
GRAVITY = 3.8
# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_RUN_ACTION = 4
FRAMES_PER_IDLE_ACTION = 6

class Ai:
    images = None

    def load_images(self):
        if Ai.images == None:
            Ai.images = load_image('pngfile/SteamMan_run.png')

    def __init__(self, x):
        self.x = x
        self.y = 110
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0

        self.tx, self.ty = 0, 0

        self.patrol_locations = [(43, 274), (1118, 274), (1050, 494), (575, 804), (235, 991), (575, 804), (1050, 494),
                                 (1118, 274)]
        self.loc_no = 0

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_RUN_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_RUN_ACTION

    def draw(self):
        if math.cos(self.dir) < 0:
           Ai.images.composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Ai.images.draw(self.x, self.y, 100, 100)
        # draw target location
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.ball_count += 1


