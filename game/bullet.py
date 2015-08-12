
import pyglet

from .resources import bullet_image
from .physicalobject import PhysicalObject

class Bullet(PhysicalObject):
    """Bullets for the Player to fire and destroy objects"""

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(img=bullet_image, *args, **kwargs)

        self.is_bullet = True
        self.score_dif = -1

    def die(self, dt):
        self.dead = True

    def check_bounds(self):
        min_x = -self.image.width/2
        min_y = -self.image.height/2
        max_x = self.screen_size[0] + self.image.width/2
        max_y = self.screen_size[1] + self.image.height/2
        if self.x < min_x:
            self.dead = True
        elif self.x > max_x:
            self.dead = True
        if self.y < min_y:
            self.dead = True
        elif self.y > max_y:
            self.dead = True
