import random

from pico2d import *
import game_framework

import game_world
from field import *
from player_1p import *
from ball import Ball
from player_AI import *
import server
# boy = None
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if boy1.pilot == 1:
                boy1.handle_event(event)
            elif boy2.pilot == 1:
                boy2.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key == SDLK_RSHIFT:
            handle_R_shift_key()


def handle_R_shift_key():
    if boy1.pilot == 1:
        boy1.bet_P = 0
        boy1.pilot *= -1
        boy2.pilot *= -1
        boy2.state_machine.cur_state = Idle
        print(boy1.state_machine.cur_state)
        if boy1.before_state == 1:
            boy2.state_machine.cur_state = Run
    if boy2.pilot == 1 and boy1.state_machine.cur_state == Idle:
        boy2.bet_P = 0
        boy1.pilot *= -1
        boy2.pilot *= -1
        boy1.state_machine.cur_state = Idle
        if boy2.before_state == 1:
            boy1.state_machine.cur_state = Run


def init():
    global boy1,boy2
    global S_P1,S_P2
    global S_Players
    running = True

    global balls
    server.balls = Ball(800,300,4)
    game_world.add_object(server.balls, 1)
    server.background = Grass()
    game_world.add_object(server.background, 0)

    S_P1 = Ai(1200, 0)
    game_world.add_object(S_P1, 1)
    S_P2 = Ai(1100,1)
    game_world.add_object(S_P2, 1)
    boy1 = Boy(1,400)
    game_world.add_object(boy1, 1)
    boy2 = Boy( -1,500)
    game_world.add_object(boy2, 1)

    # fill here

    game_world.add_collision_pair('boy.ball', boy1, None)
    game_world.add_collision_pair('boy:ball', boy1, server.balls)
    game_world.add_collision_pair('boy.ball', boy2, None)
    game_world.add_collision_pair('boy:ball', boy2, server.balls)
    game_world.add_collision_pair('boy.ball', S_P1, None)
    game_world.add_collision_pair('boy:ball', S_P1, server.balls)
    game_world.add_collision_pair('boy.ball', S_P2, None)
    game_world.add_collision_pair('boy:ball', S_P2, server.balls)

    global goalpost_A
    goalpost_A = GoalPost(20,120,0)
    game_world.add_object(goalpost_A,1)
    game_world.add_collision_pair('ball:post_a',server.balls,goalpost_A)
    global goalpost_B
    goalpost_B = GoalPost(1580,120,1)
    game_world.add_object(goalpost_B,1)
    game_world.add_collision_pair('ball:post_b',server.balls,goalpost_B)




def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

