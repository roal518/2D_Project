from pico2d import open_canvas, delay, close_canvas
import game_framework
#import play_single_mode as start_mode
import logo_mode as start_mode
#import play_multi_mode as start_mode

open_canvas(1000, 600)
game_framework.run(start_mode)
close_canvas()

