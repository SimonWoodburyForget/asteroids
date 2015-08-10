import pyglet

from .util import center_image

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

menu_background = pyglet.resource.image("menu_background.png")
center_image(menu_background)

player_image = pyglet.resource.image("player.png")
center_image(player_image)

engine_image = pyglet.resource.image("engine_flame.png")
# anchoring at a position behind the player slightly
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2

shield_image = pyglet.resource.image("shield.png")
center_image(shield_image)

bullet_sound = pyglet.resource.media("bullet.wav", streaming=False)
bullet_image = pyglet.resource.image("bullet.png")
center_image(bullet_image)


asteroids = ["asteroid" + str(i) + ".png" for i in range(0, 4)]
asteroid_images = [pyglet.resource.image(i) for i in asteroids]
center_image(asteroid_images)
