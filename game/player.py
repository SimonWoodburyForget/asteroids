import math


import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite

from . import resources
from . import physicalobject
from . import bullet
from . import shield

class Player(physicalobject.PhysicalObject):
    """Physical player object"""
    def __init__(self,*args, **kwargs):
        super().__init__(img=resources.player_image, *args, **kwargs)
        del kwargs['screen_size'] # remove screen_size for sprite usage

        self.engine_sprite = Sprite(img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False

        self.engine_sound = resources.engine_sound
        self.engine_player = pyglet.media.Player()
        self.engine_player.queue(self.engine_sound)
        self.engine_player.volume = 0
        self.engine_player.eos_action = pyglet.media.Player.EOS_LOOP

        self.shield = shield.Shield(self.batch)
        self.shield_sound = resources.shield_sound


        # vector mechanics
        self.thrust = 100.0
        self.recoil = 200.0

        # rotational mechanics
        self.max_rotation = 250
        self.rotation_speed = 0
        self.rotation_force = 2.0
        self.rotation_resistance = 2.5

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


        right = self.key_handler[key.RIGHT]
        left = self.key_handler[key.LEFT]

        def _apply_resistance(modifier=0):
            """Slows down ship rotation"""
            if self.rotation_speed < 0.0:
                self.rotation_speed += (modifier + self.rotation_resistance) * dt
            if self.rotation_speed > 0.0:
                self.rotation_speed -= (modifier + self.rotation_resistance) * dt

        if left and right:
            modifier = self.rotation_force
            _apply_resistance(modifier/2)

        elif right:
            self.rotation_speed += self.rotation_force * dt

        elif left:
            self.rotation_speed -= self.rotation_force * dt
        
        else:
            _apply_resistance()


        if self.rotation > -360:
            self.rotation += 360
        elif self.rotation < 360:
            self.rotation -= 360


        # rotate ship
        self.rotation += self.rotation_speed

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

            # smooth sound ==
            self.engine_player.play()
            if self.engine_player.volume < 1.8:
                self.engine_player.volume += 1.2 * dt
        else:
            self.engine_sprite.visible = False
            if self.engine_player.volume > 0.01:
                self.engine_player.volume -= 1.5 * dt
            else:
                self.engine_player.pause()
            # ===============



        if self.invulnerable:
            self.shield.up = True
        else:
            self.shield.up = False

        self.shield.x = self.x
        self.shield.y = self.y
        self.shield.update(dt)


        if self.key_handler[key.SPACE]:
            # fires has long has space is held
            self.fire(dt)


    """Methods that control shield invulnerability
    Can take 1 argument, deltatime(dt), invulnerability leght"""
    def set_invulnerable(self, dt=5.0):
        self.shield_sound.play()
        self.invulnerable = True

        # time to vulnerable
        pyglet.clock.schedule_once(self.set_vulnerable, dt)
    def set_vulnerable(self, dt):
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
            new_bullet = bullet.Bullet(screen_size=self.screen_size,
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
        self.engine_player.delete()
        self.invul_sprite.delete()
        super().delete()
