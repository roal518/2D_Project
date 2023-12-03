from pico2d import *
import game_framework
import play_single_mode

def init():
    global image
    image = load_image('pngfile//tjfaudtj.png')
def finish():
    global image
    del image
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key ==SDLK_s:
            game_framework.change_mode(play_single_mode)
def draw():
    clear_canvas()
    image.draw(500,300,1000,600)
    update_canvas()
def update():
    pass