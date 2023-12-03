import random

from pico2d import *
import game_framework

import game_world
from field import *
from player_1p import *
from ball import Ball
from player_2p import *
import title_mode
# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            boy1.handle_event(event)
            boy2.handle_event(event)
            S_P2.handle_event(event)
            S_P1.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:
            if S_P1.bet_P != S_P2.bet_P:
                S_P1.pilot *= -1
                S_P2.pilot *= -1
                S_P1.bet_P = 1
                S_P2.bet_P = 1
        if event.type == SDL_KEYDOWN and event.key == SDLK_RSHIFT:
            if boy1.bet_P != boy2.bet_P:
                boy1.pilot *= -1
                boy2.pilot *= -1
                boy1.bet_P = 1
                boy2.bet_P = 1

def init():
    global boy1,boy2
    global S_P1,S_P2
    global S_Players
    running = True

    server.background = Grass()
    game_world.add_object(server.background, 0)
    S_P1 = Player_2P(1,1200)
    game_world.add_object(S_P1, 1)
    S_P2 = Player_2P(-1,1100)
    game_world.add_object(S_P2, 1)
    S_Players = [S_P1,S_P2]
    boy1 = Boy(1,400)
    game_world.add_object(boy1, 1)
    boy2 = Boy(-1,500)
    game_world.add_object(boy2, 1)

    # fill here
    server.balls = Ball(800,300,4)
    game_world.add_object(server.balls, 1)

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

