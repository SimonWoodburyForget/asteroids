import pyglet

from .util import center_image

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

menu_background = pyglet.resource.image("menu_background.png")
center_image(menu_background)

player_image = pyglet.resource.image("player.png")
center_image(player_image)

engine_sound = pyglet.resource.media("rocket_effect.wav", streaming=False)
engine_image = pyglet.resource.image("engine_flame.png")
# anchoring at a position behind the player slightly
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2

shield_sound = pyglet.resource.media("energy_wip.wav", streaming=False)
shield_images = [pyglet.resource.image(
					"shield" + str(i) + ".png")
							   for i in range(0, 10)]
center_image(shield_images)

bullet_sound = pyglet.resource.media("bullet.wav", streaming=False)
bullet_image = pyglet.resource.image("bullet.png")
center_image(bullet_image)

asteroid_images = [pyglet.resource.image(
                    "asteroid" + str(i) + ".png")
                                 for i in range(0, 4)]
center_image(asteroid_images)

asteroid_particles = pyglet.resource.image('asteroid_particle.png')

explosion_sound = pyglet.resource.media("explosion.wav", streaming=False)
