import math


import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite

from . import resources
from . import physicalobject
from . import bullet


class Player(physicalobject.PhysicalObject):
    """Physical player object"""
    def __init__(self,*args, **kwargs):
        super().__init__(img=resources.player_image, *args, **kwargs)
        del kwargs['screen_bounds']
        self.engine_sprite = Sprite(img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False

        self.engine_sound = resources.engine_sound
        self.engine_player = pyglet.media.Player()
        self.engine_player.queue(self.engine_sound)
        self.engine_player.volume = 0
        self.engine_player.eos_action = pyglet.media.Player.EOS_LOOP


        self.invul_sprite = Sprite(img=resources.shield_image, *args, **kwargs)
        self.invul_sprite.scale += 1.15
        self.invul_sprite.visible = False
        self.shield_sound = resources.shield_sound


        self.thrust = 100.0
        self.recoil = 100.0
        self.rotation_speed = 100.0

        self.ship_radius = self.image.width/2

        self.key_handler = key.KeyStateHandler()
        self.event_handlers += [self, self.key_handler]

        self.score_dif = -25

        self.reacts_to_bullets = False
        self.bullet_speed = 750.0
        self.bullet_sound = resources.bullet_sound
        self.loaded = True


    def update(self, dt):
        super().update(dt)

        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotation_speed * dt
            if self.rotation < -360:
                self.rotation += 360

        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotation_speed * dt
            if self.rotation > 360:
                self.rotation -= 360


        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y

            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True

            self.engine_player.play()
            if self.engine_player.volume < 1.5:
                self.engine_player.volume += 1.2 * dt
        else:
            self.engine_sprite.visible = False
            if self.engine_player.volume > 0.01:
                self.engine_player.volume -= 1.5 * dt
            else:
                self.engine_player.pause()

        if self.invulnerable:
            self.invul_sprite.x = self.x
            self.invul_sprite.y = self.y
            self.invul_sprite.visible = True
        else:
            self.invul_sprite.visible = False

        if self.key_handler[key.SPACE]:
            # fires has long has space is held
            self.fire(dt)

    def set_invulnerable(self, t=5):
        self.shield_sound.play()
        self.invulnerable = True
        pyglet.clock.schedule_once(self.set_vulnerable, t)

    def set_vulnerable(self, t):
        self.invulnerable = False

    def fire(self, dt):
        # fires only if loaded
        if self.loaded:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.recoil * dt
            force_y = math.sin(angle_radians) * self.recoil * dt
            self.velocity_x -= force_x
            self.velocity_y -= force_y

            angle_radians = -math.radians(self.rotation)

            ship_radius = self.ship_radius
            bullet_x = self.x + math.cos(angle_radians) * ship_radius
            bullet_y = self.y + math.sin(angle_radians) * ship_radius
            new_bullet = bullet.Bullet(screen_bounds=self.screen_bounds,
                                x=bullet_x, y=bullet_y, batch=self.batch)

            bullet_vx = (self.velocity_x +
                math.cos(angle_radians) * self.bullet_speed)
            bullet_vy = (self.velocity_y +
                math.sin(angle_radians) * self.bullet_speed)
            new_bullet.velocity_x = bullet_vx
            new_bullet.velocity_y = bullet_vy

            self.bullet_sound.play()
            self.new_objects.append(new_bullet)

            # unloading gun
            self.loaded = False
            pyglet.clock.schedule_once(self.reload, 0.1)

    def reload(self, dt):
        self.loaded = True

    #def on_key_press(self, symbol, modifiers):
    ## single short fire
    #    if symbol == key.SPACE:
    #        self.fire()

    def delete(self):
        self.engine_sprite.delete()
        self.invul_sprite.delete()
        super().delete()
