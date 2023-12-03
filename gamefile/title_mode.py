from pico2d import *
import game_framework
import instruction_single
import instruction_multi
import game_world
def init():
    global image
    image = load_image('pngfile//main1.png')
def finish():
    global image
    del image
    game_world.clear()
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            game_framework.change_mode(instruction_single)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_m:
            game_framework.change_mode(instruction_multi)
def draw():
    clear_canvas()
    image.draw(500,300,1000,600)
    update_canvas()
def update():
    pass