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
            game_framework.quit()
        else:
            server.player1.handle_event(event)
            server.player2.handle_event(event)
            server.S_player1.handle_event(event)
            server.S_player2.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key == SDLK_LSHIFT:
            if server.S_player1.bet_P != server.S_player2.bet_P:
                server.S_player1.pilot *= -1
                server.S_player2.pilot *= -1
                server.S_player1.bet_P = 1
                server.S_player2.bet_P = 1
        if event.type == SDL_KEYDOWN and event.key == SDLK_RSHIFT:
            if server.player1.bet_P != server.player2.bet_P:
                server.player1.pilot *= -1
                server.player2.pilot *= -1
                server.player1.bet_P = 1
                server.player2.bet_P = 1

def init():
    global boy1,boy2
    global S_P1,S_P2
    global S_Players
    running = True

    server.background = Grass()
    game_world.add_object(server.background, 0)

    server.S_player1 = Player_2P(1,1200)
    game_world.add_object(server.S_player1, 1)
    server.S_player2 = Player_2P(-1,1100)
    game_world.add_object(server.S_player2, 1)
    server.player1 = Boy(1,400)
    game_world.add_object(server.player1, 1)
    server.player2 = Boy(-1,500)
    game_world.add_object(server.player2, 1)

    # fill here
    server.balls = Ball(800,300,4)
    game_world.add_object(server.balls, 1)

    game_world.add_collision_pair('boy.ball', server.player1, None)
    game_world.add_collision_pair('boy:ball', server.player1, server.balls)
    game_world.add_collision_pair('boy.ball', server.player2, None)
    game_world.add_collision_pair('boy:ball', server.player2, server.balls)
    game_world.add_collision_pair('boy.ball', server.S_player1, None)
    game_world.add_collision_pair('boy:ball', server.S_player1, server.balls)
    game_world.add_collision_pair('boy.ball', server.S_player2, None)
    game_world.add_collision_pair('boy:ball', server.S_player2, server.balls)


    server.goalpost_A = GoalPost(20,120,0)
    game_world.add_object(server.goalpost_A,1)
    game_world.add_collision_pair('ball:post_a',server.balls,server.goalpost_A)

    server.goalpost_B = GoalPost(1580,120,1)
    game_world.add_object(server.goalpost_B,1)
    game_world.add_collision_pair('ball:post_b',server.balls,server.goalpost_B)

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

