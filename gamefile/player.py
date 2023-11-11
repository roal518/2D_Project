# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle
from ball import Ball
import game_framework
import game_world

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def jump_to_run(e):
    return e[0] == 'DOWN'
def jump_to_idle(e):
    return e[0] == 'NO_DOWN'

# time_out = lambda e : e[0] == 'TIME_OUT'
CEILING = 300
FLOOR = 90


# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
GRAVITY = 5.8
# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
class Jump:
    @staticmethod
    def enter (boy,e):
        if space_down(e):
            boy.fly = 1
    @staticmethod
    def exit (boy, e):
        pass
    @staticmethod
    def do(boy):
        if boy.action == 2 or boy.action == 3:
               boy.state_machine.handle_event(('NO_DOWN', 0))
        elif boy.action == 0 or boy.action == 1:
               boy.state_machine.handle_event(('DOWN', 0))
    @staticmethod
    def draw(boy):
         boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Idle:

    @staticmethod
    def enter(boy, e):
        if boy.face_dir == -1:
            boy.action = 2
        elif boy.face_dir == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if boy.fly == 1:
            if not boy.is_jump:
                if boy.y <= CEILING:
                    boy.y += GRAVITY*RUN_SPEED_PPS * game_framework.frame_time
                else:
                    boy.is_jump=True
            elif  boy.is_jump:
                boy.y -= GRAVITY*RUN_SPEED_PPS * game_framework.frame_time
                if boy.y <= FLOOR:
                    boy.fly = 0
                    boy.is_jump = False
                    boy.y = FLOOR
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        draw_rectangle(*boy.get_bb())  # 튜플을 풀어헤쳐서 인자로 전달한다.


class Run:

    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.action, boy.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.action, boy.face_dir = -1, 0, -1

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600-25)
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if boy.fly == 1:
            if not boy.is_jump:
                if boy.y <= CEILING:
                    boy.y += GRAVITY*RUN_SPEED_PPS * game_framework.frame_time
                else:
                    boy.is_jump=True
            elif  boy.is_jump:
                boy.y -= GRAVITY*RUN_SPEED_PPS * game_framework.frame_time
                if boy.y <= FLOOR:
                    boy.fly = 0
                    boy.is_jump = False
                    boy.y = FLOOR
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        draw_rectangle(*boy.get_bb())  # 튜플을 풀어헤쳐서 인자로 전달한다.

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
            Jump:{jump_to_idle: Idle, jump_to_run: Run}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)





class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.fly = 0
        self.is_jump = False
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
    # fill here
    def get_bb(self):
        # return self.x - a, self.y - b, self.x + c, self.y + d
        return self.x - 20, self.y - 45, self.x + 20, self.y + 45

    def handle_collision(self, group, other):
        pass