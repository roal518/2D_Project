import random

from pico2d import *
import game_framework

import game_world
from field import *
from player_1p import *
from ball import Ball
from player_2p import *
# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            ai.handle_event(event)
            boy.handle_event(event)

def init():
    global grass
    global boy
    global ai
    running = True
    ai = Ai()
    game_world.add_object(ai, 1)

    boy = Boy()
    game_world.add_object(boy, 1)

    # fill here
    global balls
    balls = [Ball(800,300,4) for _ in range(1)]
    game_world.add_objects(balls, 1)

    game_world.add_collision_pair('boy.ball', boy, None) #소년을 등록
    for ball in balls:
        game_world.add_collision_pair('boy:ball', boy, ball)
    game_world.add_collision_pair('boy.ball', ai, None)  # 소년을 등록
    for ball in balls:
        game_world.add_collision_pair('boy:ball', ai, ball)

    global goalpost_A
    goalpost_A = GoalPost(20,120,0)
    game_world.add_object(goalpost_A,1)
    game_world.add_collision_pair('ball:post_a',ball,goalpost_A)
    global goalpost_B
    goalpost_B = GoalPost(1580,120,1)
    game_world.add_object(goalpost_B,1)
    game_world.add_collision_pair('ball:post_b',ball,goalpost_B)

    background =Background()
    game_world.add_object(background,0)

    grass = Grass()
    game_world.add_object(grass, 0)




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

