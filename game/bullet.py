
import pyglet

from .resources import bullet_image
from .physicalobject import PhysicalObject

class Bullet(PhysicalObject):
    """Bullets for the Player to fire and destroy objects"""

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(img=bullet_image, *args, **kwargs)

        pyglet.clock.schedule_once(self.die, 1)
        self.is_bullet = True
        self.score_dif = -1

    def die(self, dt):
        self.dead = True

    def check_bounds(self):
        pass # makes bullet fly off screen
