





exit()
import pyglet
from pyglet.window import key


import platform
platform_ = platform.platform()
platform.release()
platform.version()

try:
    if platform_.split('-')[6] in ['LinuxMint']:
        # fix's sound related issues on linux mint caused by PulseAudio, like:
        # Segmentation Faults - Premature sound cutting - too large exception
        pyglet.options['audio'] = ('openal', 'silent')
except:
    pass

from game import load

window = pyglet.window.Window()
screen_size = {'x':window.width, 'y':window.height}
main_batch = pyglet.graphics.Batch()


label = pyglet.text.Label(
    y=screen_size['y']/2,
    x=screen_size['x']/2,
    text='test',
    batch=main_batch)
label_dict = {'text':label.text}
label_dict['text'] = 'test 2'

# display test
#from game import resources
#pyglet.sprite.Sprite(
#    img=resources.player_image,
#    x=screen_size['x'],
#    y=screen_size['y']
#)
def on_key_press(symbol, modifers):
    if symbol == key.SPACE:
        print('space')
        return True

window.push_handlers(on_key_press)
window.push_handlers(on_key_press)
window.push_handlers(on_key_press)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print('SPACE')

window.push_handlers(on_key_press)

window.pop_handlers()
window.pop_handlers()
window.pop_handlers()
window.pop_handlers()
window.pop_handlers()


@window.event
def on_draw():
    window.clear()
    main_batch.draw()

#def update(dt):
#    player.play()
#pyglet.clock.schedule_interval(update, 1/120.0)

pyglet.app.run()
