# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *
import random
import math
import game_framework
import play_single_mode
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import server
# state event check`
# ( state event type, event value )
# time_out = lambda e : e[0] == 'TIME_OUT'
CEILING = 300
FLOOR = 90

# Boy Run Speed
PIXEL_PER_METER = (20.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0  # Km / Hour
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
    def __init__(self, x, job):
        self.job = job
        self.x = x
        self.y = 90
        self.run_images = load_image('pngfile/SteamMan_run.png')
        self.idle_images = load_image('pngfile/SteamMan_idle.png')
        self.dir = 90.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 0
        self.face_dir = -1
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()
    def get_bb(self):
        if self.face_dir == -1:
            return self.x - 8, self.y - 55, self.x + 40, self.y + 25
        elif self.face_dir == 1:
            return self.x - 40, self.y - 55, self.x + 8, self.y + 25

    def update(self):
        self.frame = (self.frame + FRAMES_PER_RUN_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_RUN_ACTION
        self.bt.run()
    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y
        if math.cos(self.dir) > 0:
            self.face_dir = 1
            if self.state == 1:
                self.run_images.clip_draw(int(self.frame) * 48, 0, 48, 48, sx, sy, 100, 100)
            else:
                self.idle_images.clip_draw(int(self.frame) * 48, 0, 48, 48, sx, sy, 100, 100)
        else:
            self.face_dir = -1
            if self.state == 1:
                self.run_images.clip_composite_draw(int(self.frame) * 48, 0, 48, 48, 0, 'h', sx, sy, 100, 100)
            else:
                self.idle_images.clip_composite_draw(int(self.frame) * 48, 0, 48, 48, 0, 'h', sx, sy, 100, 100)
        # draw target location


    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass
    def set_target_location(self,x=None,y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = play_single_mode.server.balls.x, play_single_mode.server.balls.y
        return BehaviorTree.SUCCESS
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty -self.y , tx-self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        if self.job == 1:
            self.x = clamp(900,self.x,1600)
            if self.x < 910:
                self.state = 0
            else:
                self.state = 1
        elif self.job == 0:
            self.x = clamp(90,self.x,1200)
            if self.x > 1190:
                self.state = 0
            else:
                self.state = 1

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2
    def move_to(self, r=0.5):
        self.state = 1
        self.move_slightly_to(play_single_mode.server.balls.x, play_single_mode.server.balls.y)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
    def build_behavior_tree(self):
        a1 = Action('Set target location',self.set_target_location,self.x,self.y)
        a2 = Action('Move to',self.move_to)
        root = SEQ_move_to_target_location = Sequence('Move to target location',a1,a2)
        self.bt =BehaviorTree(root)
