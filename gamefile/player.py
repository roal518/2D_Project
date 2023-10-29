# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE
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
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 2:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        if boy.fly == 1:
            if not boy.is_jump:
                if boy.y <= 220:
                    boy.y += 10
                else:
                    boy.is_jump=True
            elif  boy.is_jump:
                boy.y -= 10
                if boy.y == boy.ground:
                    boy.fly = 0
                    boy.is_jump = False

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

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
# boy.fly를 주인공 클래스에 포함시켰다. 이 함수를 이용해서 선수가 키보드 입력을 받아도 날 수 있게
# state가 변경된 곳에서도 계속 점프를 이어가도록 바꿔주자
class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        if boy.fly == 1:
            if not boy.is_jump:
                if boy.y <= 220:
                    boy.y += 10
                else:
                    boy.is_jump=True
            elif  boy.is_jump:
                boy.y -= 10
                if boy.y == boy.ground:
                    boy.fly = 0
                    boy.is_jump = False
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)





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
        self.dir = 0
        self.face_dir = 1
        self.fly = 0 # 점프 하면 1 아니면 0
        self.is_jump = False# 점프 후 천장에 닿았는가? 닿으면 True
        self.ground = 90
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
