import random

from pico2d import *
import game_framework

import game_world
from field import *
from player import *
from ball import Ball

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global grass
    global boy

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    # fill here
    global balls
    balls = [Ball(random.randint(600,800),300,4) for _ in range(5)]
    game_world.add_objects(balls, 1)

    game_world.add_collision_pair('boy.ball', boy, None) #소년을 등록
    for ball in balls:
        game_world.add_collision_pair('boy:ball', boy, ball)

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

