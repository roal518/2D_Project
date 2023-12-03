import random

from pico2d import *
import game_framework
import title_mode
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
            play_single_mode.finish()
        else:
            if server.player1.pilot == 1:
                server.player1.handle_event(event)
            elif server.player2.pilot == 1:
                server.player2.handle_event(event)
        if event.type == SDL_KEYDOWN and event.key == SDLK_RSHIFT:
            handle_R_shift_key()


def handle_R_shift_key():
    if server.player1.pilot == 1:
        server.player1.bet_P = 0
        server.player1.pilot *= -1
        server.player2.pilot *= -1
        server.player2.state_machine.cur_state = Idle
        if server.player1.before_state == 1:
            server.player2.state_machine.cur_state = Run
    if server.player2.pilot == 1 and server.player1.state_machine.cur_state == Idle:
        server.player2.bet_P = 0
        server.player1.pilot *= -1
        server.player2.pilot *= -1
        server.player1.state_machine.cur_state = Idle
        if server.player2.before_state == 1:
            server.player1.state_machine.cur_state = Run


def init():

    running = True

    global balls
    server.balls = Ball(800,300,4)
    game_world.add_object(server.balls, 1)
    server.background = Grass()
    game_world.add_object(server.background, 0)

    server.S_player1 = Ai(1200, 0)
    game_world.add_object(server.S_player1, 1)
    server.S_player2 = Ai(1100,1)
    game_world.add_object(server.S_player2, 1)

    server.player1 = Boy(1,400)
    game_world.add_object(server.player1, 1)
    server.player2 = Boy( -1,500)
    game_world.add_object(server.player2, 1)

    # fill here

    game_world.add_collision_pair('boy.ball', server.player1, None)
    game_world.add_collision_pair('boy:ball', server.player1, server.balls)
    game_world.add_collision_pair('boy.ball', server.player2, None)
    game_world.add_collision_pair('boy:ball', server.player2, server.balls)
    game_world.add_collision_pair('boy.ball', server.S_player1, None)
    game_world.add_collision_pair('boy:ball', server.S_player1, server.balls)
    game_world.add_collision_pair('boy.ball', server.S_player2, None)
    game_world.add_collision_pair('boy:ball', server.S_player2, server.balls)

    global goalpost_A
    server.goalpost_A = GoalPost(20,120,0)
    game_world.add_object(server.goalpost_A,1)
    game_world.add_collision_pair('ball:post_a',server.balls,server.goalpost_A)
    global goalpost_B
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

